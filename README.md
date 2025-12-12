# RDP Title Master

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![C# .NET 8](https://img.shields.io/badge/.NET-8.0-purple.svg)](https://dotnet.microsoft.com/)
[![Platform Windows](https://img.shields.io/badge/platform-Windows-0078d7.svg)](https://www.microsoft.com/windows)

**RDP Title Master** is a powerful background utility for System Administrators who manage multiple Remote Desktop (MSTSC) connections. It automatically identifies RDP windows based on their titles (IP/Host) and overlays a custom, color-coded "Badge" on the toolbar.

Never act on **PROD** thinking it's **TEST** again.

![Mockup](https://placehold.co/600x120/0078d7/ffffff?text=MSTSC+Toolbar+Example)

## 🌟 Key Features

*   **🕵️ Daemon Mode**: Runs in the background and constantly monitors for new RDP sessions. No need to run a script manually for every window.
*   **🧠 Auto-Matching**: Matches window titles (Hostnames or IPs) against a customizable list of rules.
*   **🎨 Visual Badges**: Renders modern, rounded badges with drop shadows.
    *   🔴 **Red** for PROD
    *   🟢 **Green** for LOCAL/DEV
    *   🔵 **Blue** for TEST
*   **🛠️ Hot-Reload**: Changes to `settings.json` are applied on the next refresh cycle (every 3 seconds).

## 🚀 Getting Started

### Prerequisites
*   Windows 10/11 or Server 2016+
*   [.NET Desktop Runtime 8.0](https://dotnet.microsoft.com/download/dotnet/8.0) (if running the compiled version).

### Installation

1.  Download the latest release (or build from source).
2.  Edit `settings.json` to define your environment rules.
3.  Run `MstscTitleBar.exe`.
4.  Open Remote Desktop connections and watch the magic happen.

## Project Structure

```text
.
├── MstscTitleBar/       # C# .NET Project (Main)
│   ├── Program.cs       # Logic & Rendering
│   ├── settings.json    # Configuration
│   └── MstscTitleBar.csproj
├── legacy_python/       # Python Version (Deprecated)
├── README.md
└── .gitignore
```

### Configuration (`settings.json`)

Map keywords found in the RDP window title to specific labels and colors.

```json
[
  {
    "Pattern": "192.168",
    "Label": "🏠 HOME LAB",
    "ColorHex": "#2ecc71"
  },
  {
    "Pattern": "db-prod",
    "Label": "🔥 PROD DB",
    "ColorHex": "#e74c3c"
  },
  {
    "Pattern": "aws",
    "Label": "☁️ AWS",
    "ColorHex": "#f39c12"
  }
]
```

## 🛠️ Building from Source

```bash
cd MstscTitleBar
dotnet restore
dotnet run
```

To build a single-file executable for easy distribution:

```bash
dotnet publish -c Release -r win-x64 --self-contained -p:PublishSingleFile=true
```

## ⚠️ Known Limitations

*   **Window Resize**: If you resize the RDP window, the overlay might disappear briefly until the daemon refreshes (every 3 seconds).
*   **Full Screen**: The toolbar in full-screen mode operates differently; this tool targets the "Windowed" mode toolbar (`BBarWindowClass`).

## License

MIT License. Free for personal and commercial use.
