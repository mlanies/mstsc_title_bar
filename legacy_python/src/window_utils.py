import ctypes
from ctypes import wintypes
import logging
from typing import Optional, Dict, Any
from src.win32_defs import (
    user32, gdi32, RECT, BLENDFUNCTION, SIZE, POINT,
    GWL_EXSTYLE, WS_EX_LAYERED, get_last_error_message
)

logger = logging.getLogger(__name__)

def find_window_by_class(class_name: str) -> Optional[int]:
    """Finds a window by its class name."""
    if not user32:
        logger.warning(f"Not running on Windows, cannot find window: {class_name}")
        return None
    
    hwnd = user32.FindWindowW(class_name, None)
    if hwnd:
        logger.info(f"Found window '{class_name}': {hwnd}")
        return hwnd
    else:
        logger.info(f"Window '{class_name}' not found.")
        return None

def find_child_window(parent_hwnd: int, class_name: str) -> Optional[int]:
    """Finds a child window with the specified class name."""
    if not user32:
        return None
        
    child_hwnd = None

    def callback(hwnd, _):
        nonlocal child_hwnd
        buffer = ctypes.create_unicode_buffer(256)
        user32.GetClassNameW(hwnd, buffer, 256)
        if buffer.value == class_name:
            child_hwnd = hwnd
            logger.info(f"Found child window: {hwnd}, ClassName={buffer.value}")
            return False  # Stop enumeration
        return True

    EnumChildProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    user32.EnumChildWindows(parent_hwnd, EnumChildProc(callback), 0)
    return child_hwnd


def make_window_transparent_with_text(hwnd: int, text: str, config: Dict[str, Any]):
    """Makes a window transparent and draws text on it."""
    if not user32 or not gdi32:
        logger.error("Win32 APIs not available.")
        return
    
    width = config.get("WIDTH", 400)
    height = config.get("HEIGHT", 100)
    margin_left = config.get("MARGIN_LEFT", 50)
    margin_top = config.get("MARGIN_TOP", 5)
    font_name = config.get("FONT_NAME", "Arial")
    font_size = config.get("FONT_SIZE", 16)
    font_weight = config.get("FONT_WEIGHT", 700)
    text_color = config.get("TEXT_COLOR", 0x00FFFFFF)
    
    # Load device context
    hdc = user32.GetDC(0)
    memdc = gdi32.CreateCompatibleDC(hdc)
    bitmap = gdi32.CreateCompatibleBitmap(hdc, width, height)
    gdi32.SelectObject(memdc, bitmap)

    # Fill background
    brush = gdi32.CreateSolidBrush(0x00000000)  # Transparent/Black
    rect = RECT(margin_left, margin_top, width - margin_left, height - margin_top)
    user32.FillRect(memdc, ctypes.byref(rect), brush)

    # Draw text
    # CreateFontW arguments: height, width, escapement, orientation, weight, italic, underline, strikeout, 
    # charset, output_precision, clip_precision, quality, pitch_and_family, face_name
    font = gdi32.CreateFontW(font_size, 0, 0, 0, font_weight, 0, 0, 0, 1, 0, 0, 0, 0, font_name)
    gdi32.SelectObject(memdc, font)
    gdi32.SetTextColor(memdc, text_color)
    gdi32.SetBkMode(memdc, 1)  # TRANSPARENT
    user32.DrawTextW(memdc, text, -1, ctypes.byref(rect), 0x0)

    # Set transparent layer
    blend = BLENDFUNCTION(0, 0, 255, 1)
    size = SIZE(width, height)
    point_source = POINT(0, 0)
    point_window = POINT(0, 0)

    # Add WS_EX_LAYERED extended style
    current_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    user32.SetWindowLongW(hwnd, GWL_EXSTYLE, current_style | WS_EX_LAYERED)
    
    result = user32.UpdateLayeredWindow(
        hwnd, 
        hdc, 
        ctypes.byref(point_window), 
        ctypes.byref(size),
        memdc, 
        ctypes.byref(point_source), 
        0, 
        ctypes.byref(blend), 
        2
    )

    # Clean up resources
    gdi32.DeleteObject(bitmap)
    gdi32.DeleteObject(brush)
    gdi32.DeleteObject(font)
    gdi32.DeleteDC(memdc)
    user32.ReleaseDC(0, hdc)

    if not result:
        logger.error(f"Failed to set transparency. Error: {get_last_error_message()}")
    else:
        logger.info(f"Transparency and text successfully applied to window {hwnd}.")
