
# Добавление информации в панель MSTSC

Этот скрипт предназначен для изменения окна `ToolbarWindow32`, которое является частью панели управления Microsoft Remote Desktop (MSTSC). Наше решение позволяет добавлять пользовательскую информацию, такую как текст заголовка, в панель MSTSC, что может быть полезно для кастомизации или отображения дополнительной информации.

## Возможности

1.  **Поиск окон**:
    
    -   Находит родительское окно с классом `BBarWindowClass`.
    -   Находит дочернее окно с классом `ToolbarWindow32`, находящееся в панели MSTSC.
2.  **Изменение стилей**:
    
    -   Добавляет стили `WS_CAPTION` (заголовок окна) и `WS_MINIMIZE` (кнопка свертывания), чтобы сделать окно более функциональным и визуально заметным.
3.  **Добавление пользовательской информации**:
    
    -   Устанавливает текст заголовка дочернего окна на `2GC` (или любой другой текст по желанию).

## Зачем это нужно?

Этот скрипт позволяет кастомизировать панель управления MSTSC, добавляя в неё текст или стили, необходимые для ваших задач. Это может быть полезно для визуализации дополнительной информации, такой как статус подключения, пользовательские метки или другие данные, связанные с удалённым рабочим столом.

## Как использовать?

1.  Убедитесь, что Python установлен на вашем компьютере.
2.  Запустите скрипт:
    
    bash
    
    Копировать код
    
    `python script_name.py` 
    
3.  После выполнения скрипта текст и стили будут автоматически добавлены в панель MSTSC.

----------

#### English

# Adding Information to MSTSC Toolbar

This script is designed to modify the `ToolbarWindow32` window, which is part of the Microsoft Remote Desktop (MSTSC) toolbar. Our solution allows adding custom information, such as title text, to the MSTSC toolbar, which can be useful for customization or displaying additional details.

## Features

1.  **Window Search**:
    
    -   Locates the parent window with the class `BBarWindowClass`.
    -   Finds the child window with the class `ToolbarWindow32` within the MSTSC toolbar.
2.  **Style Modification**:
    
    -   Adds `WS_CAPTION` (window title) and `WS_MINIMIZE` (minimize button) styles to make the window more functional and visually noticeable.
3.  **Adding Custom Information**:
    
    -   Sets the title text of the child window to `2GC` (or any custom text as needed).

## Why Use This Script?

This script enables customization of the MSTSC toolbar by adding text or styles required for your specific needs. It can be useful for displaying additional information, such as connection status, custom labels, or other data related to remote desktop sessions.

## How to Use?

1.  Ensure Python is installed on your computer.
2.  Run the script:
    
    bash
    
    Копировать код
    
    `python script_name.py` 
    
3.  After execution, the text and styles will be automatically applied to the MSTSC toolbar.
