
# [Demo: Customizing MSTSC Toolbar Title](https://pub-a89b5697d4074daeb851dc6c011ed225.r2.dev/mstsc_title_new.mp4)


## Добавление пользовательской информации в панель MSTSC

Этот скрипт позволяет кастомизировать панель управления Microsoft Remote Desktop (MSTSC), изменяя окно `ToolbarWindow32`, которое отвечает за отображение панели инструментов. В частности, он добавляет текст и настраивает стиль окна, что делает панель более информативной и визуально заметной.

### Основные возможности

1.  **Поиск окон:**
    
    -   Автоматически находит родительское окно с классом `BBarWindowClass`.
    -   Определяет дочернее окно с классом `ToolbarWindow32`, которое отвечает за панель инструментов MSTSC.
2.  **Добавление пользовательского текста:**
    
    -   Позволяет установить текст, например, `2GC - test server`, или любой другой, чтобы отображать пользовательскую информацию в панели.
3.  **Настройка стилей окна:**
    
    -   Добавляет стили, такие как `WS_CAPTION` (заголовок окна) и `WS_MINIMIZE` (кнопка свертывания), чтобы сделать окно более функциональным.
4.  **Прозрачный фон и отрисовка текста:**
    
    -   Устанавливает прозрачный фон панели инструментов и добавляет текст с кастомными параметрами (шрифт, размер, цвет и позиция).

----------

### Для чего это нужно?

Этот скрипт разработан для пользователей, которые хотят улучшить панель MSTSC, добавляя текстовую информацию или изменяя стили окна. Это особенно полезно для:

-   Отображения статуса подключения.
-   Идентификации сессий удалённого рабочего стола.
-   Добавления пользовательских меток или любой другой дополнительной информации.

----------

### Как это работает?

1.  **Python-скрипт запускается на локальном компьютере.**
2.  **Автоматически обнаруживаются окна панели MSTSC.**
3.  **В окно панели добавляются текст и стили, заданные пользователем.**

----------

### Инструкция по установке и запуску

1.  Убедитесь, что у вас установлен Python 3.8 или выше.
    
2.  Клонируйте репозиторий:
    
    bash
    
    Копировать код
    
    `git clone https://github.com/your-repo/mstsc-customization.git
    cd mstsc-customization` 
    
3.  Запустите скрипт:
    
    bash
    
    Копировать код
    
    `python script_name.py` 
    
4.  Откройте MSTSC, чтобы увидеть изменения на панели.
    

----------

### Пример использования

**Пример использования скрипта:**

-   Текущий текст, добавленный на панель: `2GC - test server`.
-   Отступы, шрифт и размер текста задаются внутри кода.
-   Установлен прозрачный фон панели инструментов.

----------


## Adding Custom Information to the MSTSC Toolbar

This script customizes the Microsoft Remote Desktop (MSTSC) toolbar by modifying the `ToolbarWindow32` window, which controls the toolbar display. Specifically, it adds custom text and adjusts the window's style to make the toolbar more informative and visually distinct.

### Key Features

1.  **Window Detection:**
    
    -   Automatically locates the parent window with the class `BBarWindowClass`.
    -   Identifies the child window with the class `ToolbarWindow32`, responsible for the MSTSC toolbar.
2.  **Adding Custom Text:**
    
    -   Allows you to set custom text, such as `2GC - test server`, or any other information you want to display on the toolbar.
3.  **Window Style Customization:**
    
    -   Adds styles such as `WS_CAPTION` (window title) and `WS_MINIMIZE` (minimize button) to enhance functionality.
4.  **Transparent Background and Text Rendering:**
    
    -   Sets a transparent background for the toolbar and renders text with custom parameters (font, size, color, and position).

----------

### Why Use This Script?

This script is designed for users who want to enhance the MSTSC toolbar by adding custom text or modifying window styles. It is particularly useful for:

-   Displaying connection status.
-   Identifying remote desktop sessions.
-   Adding custom labels or any additional information.

----------

### How It Works

1.  **Run the Python script on your local machine.**
2.  **The script automatically detects MSTSC toolbar windows.**
3.  **Custom text and styles are applied to the toolbar window as configured.**

----------

### Installation and Usage

1.  Ensure Python 3.8 or later is installed on your machine.
    
2.  Clone the repository:
    
    bash
    
    Копировать код
    
    `git clone https://github.com/your-repo/mstsc-customization.git
    cd mstsc-customization` 
    
3.  Run the script:
    
    bash
    
    Копировать код
    
    `python script_name.py` 
    
4.  Open MSTSC to see the changes applied to the toolbar.
    

----------

### Example Usage

**Example script behavior:**

-   Current text added to the toolbar: `2GC - test server`.
-   Margins, font, and text size are configurable within the script.
-   A transparent background is applied to the toolbar for a cleaner look.
