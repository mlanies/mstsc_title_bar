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
WM_SETTEXT = 0x000C


user32 = ctypes.WinDLL("user32", use_last_error=True)

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

def set_window_styles(hwnd, styles_to_add):
    """Добавляет стили окну."""
    current_style = user32.GetWindowLongW(hwnd, GWL_STYLE)
    if current_style == 0:
        print(f"Не удалось получить стили окна {hwnd}. Ошибка: {get_last_error_message()}")
        return
    new_style = current_style | styles_to_add
    if user32.SetWindowLongW(hwnd, GWL_STYLE, new_style) == 0:
        print(f"Не удалось установить стили окна {hwnd}. Ошибка: {get_last_error_message()}")
        return
    if not user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, SWP_FRAMECHANGED | SWP_NOZORDER | SWP_NOSIZE | SWP_NOMOVE):
        print(f"Не удалось обновить стили окна {hwnd}. Ошибка: {get_last_error_message()}")
    else:
        print(f"Обновлены стили окна {hwnd}: {hex(current_style)} -> {hex(new_style)}")

def set_window_text(hwnd, text):
    """Устанавливает текст заголовка окна."""
    if user32.SetWindowTextW(hwnd, text):
        print(f"Текст окна {hwnd} успешно изменен на: {text}")
    else:
        print(f"Не удалось изменить текст окна {hwnd}. Ошибка: {get_last_error_message()}")

def set_window_position_and_size(hwnd, x_offset, width, height):
    """
    Устанавливает положение окна (сдвиг по горизонтали) и размер.
    x_offset: Сдвиг окна влево, передайте отрицательное значение для смещения.
    """
    rect = wintypes.RECT()
    if user32.GetWindowRect(hwnd, ctypes.byref(rect)):
        # Размеры экрана
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)

        # Новая позиция
        x = rect.left + x_offset
        y = rect.top

        # Проверка на границы экрана
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x + width > screen_width:
            x = screen_width - width
        if y + height > screen_height:
            y = screen_height - height

        if user32.SetWindowPos(hwnd, None, x, y, width, height, SWP_NOZORDER):
            print(f"Положение и размеры окна {hwnd} успешно изменены на: x={x}, y={y}, width={width}, height={height}")
        else:
            print(f"Не удалось изменить положение и размеры окна {hwnd}. Ошибка: {get_last_error_message()}")
    else:
        print(f"Не удалось получить координаты окна {hwnd}. Ошибка: {get_last_error_message()}")

def modify_toolbar_window():
    # Найти родительское окно BBarWindowClass
    parent_hwnd = find_window_by_class("BBarWindowClass")
    if not parent_hwnd:
        print("Родительское окно не найдено.")
        return

    # Установить новый текст для родительского окна
    set_window_text(parent_hwnd, "Мой заголовок")

    # Найти дочернее окно ToolbarWindow32
    child_hwnd = find_child_window(parent_hwnd, "ToolbarWindow32")
    if not child_hwnd:
        print("Дочернее окно ToolbarWindow32 не найдено.")
        return

    # Изменить стили дочернего окна
    set_window_styles(child_hwnd, WS_CAPTION | WS_MINIMIZE)

    # Установить размеры и сдвинуть окно влево
    set_window_position_and_size(child_hwnd, x_offset=-400, width=144, height=26)

    # Установить текст дочернего окна
    set_window_text(child_hwnd, "2GC - test server")

if __name__ == "__main__":
    modify_toolbar_window()
