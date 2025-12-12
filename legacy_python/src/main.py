import logging
from src.window_utils import find_window_by_class, find_child_window, make_window_transparent_with_text

# Configuration
CONFIG = {
    "WINDOW_TEXT": "2GC - test server",
    "FONT_NAME": "Arial",
    "FONT_SIZE": 16,
    "FONT_WEIGHT": 700,
    "TEXT_COLOR": 0x00FFFFFF,
    "BG_COLOR": 0x00000000,
    "WIDTH": 400,
    "HEIGHT": 100,
    "MARGIN_LEFT": 50,
    "MARGIN_TOP": 5,
}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting MSTSC Toolbar Customizer...")
    parent = find_window_by_class("BBarWindowClass")
    if not parent:
        logger.error("Parent window BBarWindowClass not found. Is Remote Desktop running?")
        return

    child = find_child_window(parent, "ToolbarWindow32")
    if not child:
        logger.error("Child window ToolbarWindow32 not found.")
        return

    make_window_transparent_with_text(child, CONFIG["WINDOW_TEXT"], CONFIG)
    logger.info("Done.")

if __name__ == "__main__":
    main()
