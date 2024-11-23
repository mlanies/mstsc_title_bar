import ctypes
from ctypes import wintypes

# Константы
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
SWP_FRAMECHANGED = 0x0020
SWP_NOZORDER = 0x0004
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
LWA_COLORKEY = 0x01
LWA_ALPHA = 0x02

# Библиотеки
user32 = ctypes.WinDLL("user32", use_last_error=True)
gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)

# Структуры
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

def get_last_error_message():
    """Возвращает сообщение об ошибке."""
    error_code = ctypes.get_last_error()
    if error_code:
        buffer = ctypes.create_unicode_buffer(256)
        ctypes.windll.kernel32.FormatMessageW(
            0x00001000,
            None,
            error_code,
            0,
            buffer,
            256,
            None
        )
        return buffer.value
    return "Нет ошибок"

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

def make_window_transparent_with_text(hwnd, text, width=400, height=100):
    """Делает окно прозрачным и рисует текст."""
    # Загрузка контекста устройства
    hdc = user32.GetDC(0)
    memdc = gdi32.CreateCompatibleDC(hdc)
    bitmap = gdi32.CreateCompatibleBitmap(hdc, width, height)
    gdi32.SelectObject(memdc, bitmap)

    # Заполнение фона
    brush = gdi32.CreateSolidBrush(0x00000000)  # Черный прозрачный
    rect = RECT(50, 5, width - 50, height - 5)  # Отступ 50 пикселей слева
    user32.FillRect(memdc, ctypes.byref(rect), brush)

    # Рисуем текст
    font = gdi32.CreateFontW(16, 0, 0, 0, 700, 0, 0, 0, 1, 0, 0, 0, 0, "Arial")  # Размер шрифта 16
    gdi32.SelectObject(memdc, font)
    gdi32.SetTextColor(memdc, 0x00FFFFFF)  # Белый текст
    gdi32.SetBkMode(memdc, 1)  # TRANSPARENT
    user32.DrawTextW(memdc, text, -1, ctypes.byref(rect), 0x0)

    # Установка прозрачного фона
    blend = BLENDFUNCTION(0, 0, 255, 1)
    size = SIZE(width, height)
    point_source = POINT(0, 0)
    point_window = POINT(0, 0)

    user32.SetWindowLongW(hwnd, GWL_EXSTYLE, user32.GetWindowLongW(hwnd, GWL_EXSTYLE) | WS_EX_LAYERED)
    result = user32.UpdateLayeredWindow(hwnd, hdc, ctypes.byref(point_window), ctypes.byref(size),
                                        memdc, ctypes.byref(point_source), 0, ctypes.byref(blend), 2)

    # Освобождение ресурсов
    gdi32.DeleteObject(bitmap)
    gdi32.DeleteObject(brush)
    gdi32.DeleteObject(font)
    gdi32.DeleteDC(memdc)
    user32.ReleaseDC(0, hdc)

    if not result:
        print(f"Не удалось установить прозрачность. Ошибка: {get_last_error_message()}")
    else:
        print(f"Прозрачность успешно установлена для окна {hwnd}.")

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

    # Сделать окно прозрачным и нарисовать текст
    make_window_transparent_with_text(child_hwnd, "2GC - test server", width=400, height=100)

if __name__ == "__main__":
    modify_toolbar_window()
