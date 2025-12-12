using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Text;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Text.Json;
using System.Threading;

namespace MstscTitleBar
{
    // --- Data Structures ---
    public class LabelConfig
    {
        public string Pattern { get; set; } = "";
        public string Label { get; set; } = "RDP";
        public string ColorHex { get; set; } = "#000000";
    }

    class Program
    {
        private const string SETTINGS_FILE = "settings.json";
        private static List<LabelConfig> _configs = new();
        
        // Cache to avoid spamming logs or redundant updates (optional optimization)
        private static HashSet<IntPtr> _processedWindows = new HashSet<IntPtr>();

        static void Main(string[] args)
        {
            Console.WriteLine("=== MSTSC Title Bar Daemon 2.0 ===");
            
            LoadConfig();
            
            Console.WriteLine("Daemon started. Monitoring RDP windows... (Press Ctrl+C to stop)");
            Console.WriteLine($"Loaded {_configs.Count} rules.");

            // Main Loop (Daemon)
            while (true)
            {
                try
                {
                    ProcessWindows();
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Iteration Error: {ex.Message}");
                }

                Thread.Sleep(3000); // Check every 3 seconds
            }
        }

        private static void LoadConfig()
        {
            if (File.Exists(SETTINGS_FILE))
            {
                try
                {
                    string json = File.ReadAllText(SETTINGS_FILE);
                    _configs = JsonSerializer.Deserialize<List<LabelConfig>>(json) ?? new();
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error reading settings.json: {ex.Message}");
                }
            }
            else
            {
                Console.WriteLine("settings.json not found. Creating default.");
                _configs = new List<LabelConfig>
                {
                    new LabelConfig { Pattern = "192.168", Label = "HOME", ColorHex = "#2ecc71" }
                };
            }
        }

        private static void ProcessWindows()
        {
            // Reset state if needed, or just iterate all current top-level windows
            EnumWindowProc callback = (hwnd, lParam) =>
            {
                if (IsRdpWindow(hwnd))
                {
                    string title = GetWindowTitle(hwnd);
                    
                    // Match Title against Config
                    var rule = _configs.FirstOrDefault(c => title.Contains(c.Pattern, StringComparison.OrdinalIgnoreCase));
                    if (rule != null)
                    {
                        // Find the toolbar inside this RDP window
                        IntPtr hBBar = FindChildByClass(hwnd, "BBarWindowClass");
                        if (hBBar != IntPtr.Zero)
                        {
                            IntPtr hToolbar = FindChildByClass(hBBar, "ToolbarWindow32");
                            if (hToolbar != IntPtr.Zero)
                            {
                                // Apply the overlay
                                ApplyOverlay(hToolbar, rule);
                            }
                        }
                    }
                }
                return true; // Continue enumeration
            };

            EnumWindows(callback, IntPtr.Zero);
        }

        private static bool IsRdpWindow(IntPtr hwnd)
        {
            // Main RDP Window Class usually: TscShellContainerClass
            string className = GetClassName(hwnd);
            return className == "TscShellContainerClass";
        }

        private static void ApplyOverlay(IntPtr hwnd, LabelConfig rule)
        {
            // Force Style
            int exStyle = GetWindowLong(hwnd, GWL_EXSTYLE);
            if ((exStyle & WS_EX_LAYERED) == 0)
            {
                SetWindowLong(hwnd, GWL_EXSTYLE, exStyle | WS_EX_LAYERED);
            }

            // Dimensions
            int width = 500;
            int height = 60;

            // Colors
            Color badgeColor;
            try { badgeColor = ColorTranslator.FromHtml(rule.ColorHex); }
            catch { badgeColor = Color.Blue; }

            using (Bitmap bmp = new Bitmap(width, height))
            using (Graphics g = Graphics.FromImage(bmp))
            {
                g.SmoothingMode = SmoothingMode.AntiAlias;
                g.TextRenderingHint = TextRenderingHint.AntiAliasGridFit;

                g.Clear(Color.Transparent);

                // Draw Badge (Rounded Pill)
                string text = rule.Label;
                int fontSize = 14;
                using (Font font = new Font("Segoe UI", fontSize, FontStyle.Bold))
                {
                    SizeF textSize = g.MeasureString(text, font);
                    int paddingX = 15;
                    int paddingY = 6;
                    
                    Rectangle badgeRect = new Rectangle(20, 5, (int)textSize.Width + (paddingX * 2), (int)textSize.Height + (paddingY * 2));
                    
                    // Shadow
                    using (Brush shadowBrush = new SolidBrush(Color.FromArgb(60, 0, 0, 0)))
                    {
                         FillRoundedRectangle(g, shadowBrush, new Rectangle(badgeRect.X + 2, badgeRect.Y + 2, badgeRect.Width, badgeRect.Height), 10);
                    }

                    // Background
                    using (Brush bgBrush = new SolidBrush(badgeColor))
                    {
                        FillRoundedRectangle(g, bgBrush, badgeRect, 10);
                    }

                    // Text
                    using (Brush textBrush = new SolidBrush(Color.White))
                    {
                        g.DrawString(text, font, textBrush, badgeRect.X + paddingX, badgeRect.Y + paddingY);
                    }
                }

                UpdateLayeredWindowFromBitmap(hwnd, bmp);
            }
        }

        // --- Helper for Rounded Rect ---
        public static void FillRoundedRectangle(Graphics g, Brush brush, Rectangle bounds, int cornerRadius)
        {
            if (g == null) throw new ArgumentNullException("g");
            if (brush == null) throw new ArgumentNullException("brush");

            using (GraphicsPath path = new GraphicsPath())
            {
                path.AddArc(bounds.X, bounds.Y, cornerRadius * 2, cornerRadius * 2, 180, 90);
                path.AddArc(bounds.X + bounds.Width - cornerRadius * 2, bounds.Y, cornerRadius * 2, cornerRadius * 2, 270, 90);
                path.AddArc(bounds.X + bounds.Width - cornerRadius * 2, bounds.Y + bounds.Height - cornerRadius * 2, cornerRadius * 2, cornerRadius * 2, 0, 90);
                path.AddArc(bounds.X, bounds.Y + bounds.Height - cornerRadius * 2, cornerRadius * 2, cornerRadius * 2, 90, 90);
                path.CloseFigure();
                g.FillPath(brush, path);
            }
        }

        // --- WinAPI ---
        
        private static void UpdateLayeredWindowFromBitmap(IntPtr hwnd, Bitmap bmp)
        {
            IntPtr screenDc = GetDC(IntPtr.Zero);
            IntPtr memDc = CreateCompatibleDC(screenDc);
            IntPtr hBitmap = IntPtr.Zero;
            IntPtr oldBitmap = IntPtr.Zero;

            try
            {
                hBitmap = bmp.GetHbitmap(Color.FromArgb(0));
                oldBitmap = SelectObject(memDc, hBitmap);
                SIZE size = new SIZE { cx = bmp.Width, cy = bmp.Height };
                POINT pointSource = new POINT { x = 0, y = 0 };
                POINT topPos = new POINT { x = 0, y = 0 };
                BLENDFUNCTION blend = new BLENDFUNCTION { BlendOp = 0, BlendFlags = 0, SourceConstantAlpha = 255, AlphaFormat = 1 }; // AC_SRC_ALPHA

                UpdateLayeredWindow(hwnd, screenDc, ref topPos, ref size, memDc, ref pointSource, 0, ref blend, 2); // ULW_ALPHA
            }
            finally
            {
                ReleaseDC(IntPtr.Zero, screenDc);
                if (hBitmap != IntPtr.Zero) { SelectObject(memDc, oldBitmap); DeleteObject(hBitmap); }
                DeleteDC(memDc);
            }
        }

        private static IntPtr FindChildByClass(IntPtr parent, string className)
        {
            IntPtr result = IntPtr.Zero;
            EnumChildProc childProc = (h, l) => {
                if (GetClassName(h) == className) { result = h; return false; }
                return true;
            };
            EnumChildWindows(parent, childProc, IntPtr.Zero);
            return result;
        }

        private delegate bool EnumWindowProc(IntPtr hWnd, IntPtr lParam);
        private delegate bool EnumChildProc(IntPtr hwnd, IntPtr lParam);

        [DllImport("user32.dll")] private static extern bool EnumWindows(EnumWindowProc lpEnumFunc, IntPtr lParam);
        [DllImport("user32.dll")] private static extern bool EnumChildWindows(IntPtr hWndParent, EnumChildProc lpEnumFunc, IntPtr lParam);
        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)] private static extern int GetClassName(IntPtr hWnd, StringBuilder lpClassName, int nMaxCount);
        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)] private static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);
        [DllImport("user32.dll")] private static extern int GetWindowLong(IntPtr hWnd, int nIndex);
        [DllImport("user32.dll")] private static extern int SetWindowLong(IntPtr hWnd, int nIndex, int dwNewLong);
        [DllImport("user32.dll", SetLastError = true)] private static extern bool UpdateLayeredWindow(IntPtr hwnd, IntPtr hdcDst, ref POINT pptDst, ref SIZE psize, IntPtr hdcSrc, ref POINT pptSrc, int crKey, ref BLENDFUNCTION pblend, int dwFlags);
        [DllImport("user32.dll")] private static extern IntPtr GetDC(IntPtr hWnd);
        [DllImport("user32.dll")] private static extern int ReleaseDC(IntPtr hWnd, IntPtr hDC);
        [DllImport("gdi32.dll")] private static extern IntPtr CreateCompatibleDC(IntPtr hDC);
        [DllImport("gdi32.dll")] private static extern bool DeleteDC(IntPtr hDC);
        [DllImport("gdi32.dll")] private static extern bool DeleteObject(IntPtr hObject);
        [DllImport("gdi32.dll")] private static extern IntPtr SelectObject(IntPtr hDC, IntPtr hObject);

        private static string GetClassName(IntPtr hWnd) { var sb = new StringBuilder(256); GetClassName(hWnd, sb, sb.Capacity); return sb.ToString(); }
        private static string GetWindowTitle(IntPtr hWnd) { var sb = new StringBuilder(256); GetWindowText(hWnd, sb, sb.Capacity); return sb.ToString(); }

        private const int GWL_EXSTYLE = -20;
        private const int WS_EX_LAYERED = 0x80000;

        [StructLayout(LayoutKind.Sequential)] private struct POINT { public int x; public int y; }
        [StructLayout(LayoutKind.Sequential)] private struct SIZE { public int cx; public int cy; }
        [StructLayout(LayoutKind.Sequential)] private struct BLENDFUNCTION { public byte BlendOp; public byte BlendFlags; public byte SourceConstantAlpha; public byte AlphaFormat; }
    }
}
