import ctypes
from ctypes import wintypes

# Загрузка Windows API
user32 = ctypes.WinDLL('user32', use_last_error=True)

GetWindowLong = user32.GetWindowLongW
GetWindowLong.argtypes = [wintypes.HWND, ctypes.c_int]
GetWindowLong.restype = ctypes.c_long

SetWindowLong = user32.SetWindowLongW
SetWindowLong.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_long]
SetWindowLong.restype = ctypes.c_long

SetWindowText = user32.SetWindowTextW
SetWindowText.argtypes = [wintypes.HWND, wintypes.LPCWSTR]
SetWindowText.restype = wintypes.BOOL

UpdateWindow = user32.UpdateWindow
UpdateWindow.argtypes = [wintypes.HWND]
UpdateWindow.restype = wintypes.BOOL

EnumWindows = user32.EnumWindows
EnumWindows.argtypes = [ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM), wintypes.LPARAM]
EnumWindows.restype = wintypes.BOOL

GetClassName = user32.GetClassNameW
GetClassName.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
GetClassName.restype = ctypes.c_int

SetLayeredWindowAttributes = user32.SetLayeredWindowAttributes
SetLayeredWindowAttributes.argtypes = [wintypes.HWND, wintypes.DWORD, wintypes.BYTE, wintypes.DWORD]
SetLayeredWindowAttributes.restype = wintypes.BOOL

SetWindowPos = user32.SetWindowPos
SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
SetWindowPos.restype = wintypes.BOOL

SWP_FRAMECHANGED = 0x0020
SWP_NOZORDER = 0x0004
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002

GWL_STYLE = -16
GWL_EXSTYLE = -20
LWA_ALPHA = 0x00000002
LWA_COLORKEY = 0x00000001

WS_VISIBLE = 0x10000000
WS_CAPTION = 0x00C00000
WS_MINIMIZE = 0x20000000
WS_EX_LAYERED = 0x00080000


# Поиск окна по классу
def find_window_by_class(target_class):
    result = []

    def callback(hwnd, _):
        class_name_buf = ctypes.create_unicode_buffer(256)
        GetClassName(hwnd, class_name_buf, 256)
        if class_name_buf.value == target_class:
            result.append(hwnd)
            return False  # Остановить поиск
        return True

    proc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)(callback)
    EnumWindows(proc, 0)
    return result[0] if result else None


# Устанавливаем прозрачность окна
def make_window_transparent(hwnd, alpha=200):
    ex_style = GetWindowLong(hwnd, GWL_EXSTYLE)
    SetWindowLong(hwnd, GWL_EXSTYLE, ex_style | WS_EX_LAYERED)
    if SetLayeredWindowAttributes(hwnd, 0, alpha, LWA_ALPHA):
        print(f"Прозрачность установлена: {alpha}")
    else:
        print("Не удалось установить прозрачность.")


# Основной скрипт
if __name__ == "__main__":
    target_class = "BBarWindowClass"
    new_title = "2GC"

    print("Поиск окна...")
    hwnd = find_window_by_class(target_class)

    if hwnd:
        print(f"Окно найдено: {hwnd}")

        # Получаем текущие стили окна
        current_style = GetWindowLong(hwnd, GWL_STYLE)
        print(f"Текущий стиль окна: {hex(current_style)}")

        # Добавляем WS_CAPTION и делаем окно видимым
        new_style = current_style | WS_CAPTION
        SetWindowLong(hwnd, GWL_STYLE, new_style)

        # Обновляем окно
        SetWindowPos(hwnd, None, 0, 0, 0, 0, SWP_FRAMECHANGED | SWP_NOZORDER | SWP_NOSIZE | SWP_NOMOVE)
        UpdateWindow(hwnd)

        # Меняем текст заголовка
        if SetWindowText(hwnd, new_title):
            print(f"Текст окна успешно изменен на: {new_title}")
        else:
            print("Не удалось изменить текст окна.")

        # Устанавливаем прозрачность
        make_window_transparent(hwnd, alpha=200)
    else:
        print(f"Окно класса '{target_class}' не найдено.")
