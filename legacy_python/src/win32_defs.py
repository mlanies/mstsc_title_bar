import ctypes
from ctypes import wintypes
import sys

# Constants
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
SWP_FRAMECHANGED = 0x0020
SWP_NOZORDER = 0x0004
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
LWA_COLORKEY = 0x01
LWA_ALPHA = 0x02

# Load DLLs safely
if sys.platform == "win32":
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
else:
    # Mocks for non-Windows systems to allow linting/importing
    user32 = None  # type: ignore
    gdi32 = None   # type: ignore
    kernel32 = None # type: ignore

def get_last_error_message():
    """Returns the error message for the last error."""
    if sys.platform != "win32":
        return "Not on Windows"
    
    error_code = ctypes.get_last_error()
    if error_code:
        buffer = ctypes.create_unicode_buffer(256)
        kernel32.FormatMessageW(
            0x00001000,
            None,
            error_code,
            0,
            buffer,
            256,
            None
        )
        return buffer.value
    return "No error"

# Structures
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

class SIZE(ctypes.Structure):
    _fields_ = [("cx", ctypes.c_long), ("cy", ctypes.c_long)]

class BLENDFUNCTION(ctypes.Structure):
    _fields_ = [("BlendOp", ctypes.c_byte),
                ("BlendFlags", ctypes.c_byte),
                ("SourceConstantAlpha", ctypes.c_byte),
                ("AlphaFormat", ctypes.c_byte)]

class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long)]
