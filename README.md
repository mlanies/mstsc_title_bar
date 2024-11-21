# Window Manipulation Script

## Описание
Этот проект представляет собой Python-скрипт, предназначенный для изменения атрибутов окон в операционной системе Windows с использованием WinAPI. Скрипт был создан для манипуляции окнами, такими как окна удаленного рабочего стола (RDP), чтобы изменить заголовок, стиль, видимость и другие параметры окна.

### Возможности
- Поиск окна по классу.
- Изменение текста заголовка окна.
- Добавление стиля `WS_CAPTION` для отображения заголовка.
- Манипуляции с видимостью окна через стили.
- Основы для работы с прозрачностью окон (функциональность отключена).

### Использование
1. Убедитесь, что у вас установлен Python 3.x.
2. Запустите скрипт, указав название класса окна, которое вы хотите изменить.
3. Скрипт автоматически найдет окно и применит изменения.

### Применение
Этот скрипт был разработан для специфической задачи изменения интерфейса окна в контексте работы с RDP. Например, для добавления пользовательского заголовка окна и изменения его внешнего вида.

---

## Description
This project is a Python script designed to modify window attributes on Windows operating systems using the WinAPI. The script is tailored for manipulating windows, such as Remote Desktop (RDP) windows, to change the title, style, visibility, and other properties.

### Features
- Locate a window by its class name.
- Change the window's title text.
- Add the `WS_CAPTION` style to display a title bar.
- Modify window visibility through styles.
- Foundation for window transparency functionality (currently disabled).

### Usage
1. Ensure you have Python 3.x installed.
2. Run the script with the class name of the window you want to modify.
3. The script will automatically locate the window and apply the changes.

### Use Case
This script was developed for a specific task of modifying the appearance of a window in the context of RDP. For instance, adding a custom window title and altering its visual style.
