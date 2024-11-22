import ctypes
from ctypes import wintypes

# Константы
GWL_STYLE = -16
WS_CAPTION = 0x00C00000
WS_MINIMIZE = 0x20000000
SWP_FRAMECHANGED = 0x0020
SWP_NOZORDER = 0x0004
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002

user32 = ctypes.WinDLL("user32", use_last_error=True)

def find_window_by_class(class_name):
    """Находит окно по имени класса."""
    hwnd = user32.FindWindowW(class_name, None)
    if hwnd:
        print(f"Окно с классом {class_name} найдено: {hwnd}")
    else:
        print(f"Окно с классом {class_name} не найдено.")
    return hwnd

def find_child_window(parent_hwnd, class_name):
    """Находит дочернее окно с указанным классом."""
    child_hwnd = None

    def callback(hwnd, _):
        nonlocal child_hwnd
        buffer = ctypes.create_unicode_buffer(256)
        user32.GetClassNameW(hwnd, buffer, 256)
        if buffer.value == class_name:
            child_hwnd = hwnd
            print(f"Дочернее окно найдено: {hwnd}, ClassName={buffer.value}")
            return False  # Останавливаем поиск
        return True

    EnumChildProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    user32.EnumChildWindows(parent_hwnd, EnumChildProc(callback), 0)
    return child_hwnd

def set_window_styles(hwnd, styles_to_add):
    """Добавляет стили окну."""
    current_style = user32.GetWindowLongW(hwnd, GWL_STYLE)
    new_style = current_style | styles_to_add
    user32.SetWindowLongW(hwnd, GWL_STYLE, new_style)
    user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, SWP_FRAMECHANGED | SWP_NOZORDER | SWP_NOSIZE | SWP_NOMOVE)
    print(f"Обновлены стили окна {hwnd}: {hex(current_style)} -> {hex(new_style)}")

def set_window_text(hwnd, text):
    """Устанавливает текст заголовка окна."""
    if user32.SetWindowTextW(hwnd, text):
        print(f"Текст окна {hwnd} успешно изменен на: {text}")
    else:
        print(f"Не удалось изменить текст окна {hwnd}.")

def modify_toolbar_window():
    # Найти родительское окно BBarWindowClass
    parent_hwnd = find_window_by_class("BBarWindowClass")
    if not parent_hwnd:
        print("Родительское окно не найдено.")
        return

    # Найти дочернее окно ToolbarWindow32
    child_hwnd = find_child_window(parent_hwnd, "ToolbarWindow32")
    if not child_hwnd:
        print("Дочернее окно ToolbarWindow32 не найдено.")
        return

    # Изменить стили и текст дочернего окна
    set_window_styles(child_hwnd, WS_CAPTION | WS_MINIMIZE)
    set_window_text(child_hwnd, "2GC")

if __name__ == "__main__":
    modify_toolbar_window()
