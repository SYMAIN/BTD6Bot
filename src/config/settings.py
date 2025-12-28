# config/settings.py
import os
from dataclasses import dataclass
from pathlib import Path
import pyautogui


@dataclass
class Settings:
    # Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    SRC_DIR = BASE_DIR / "src"
    ASSETS_DIR = BASE_DIR / "assets"
    DEBUG_DIR = ASSETS_DIR / "debug"
    DATA_DIR = BASE_DIR / SRC_DIR / "data"

    # Tesseract path (OS-agnostic)
    TESSERACT_PATH = os.getenv("TESSERACT_PATH", r"X:\Tesseract\tesseract.exe")

    # Game settings
    DIFFICULTY = "medium"
    CAPTURE_INTERVAL = 5.0
    SCREEN_RES = pyautogui.size()

    # Screen settings
    # Game shifts the UI based on resolution
    UI_POSITIONS = {
        (1920, 1080): {
            "health": (20, 60, 140, 290),  # y1, y2, x1, x2
            "gold": (20, 60, 370, 650),
            "round": (30, 75, 1400, 1560),
        },
        (1920, 1200): {
            "health": (70, 110, 135, 285),
            "gold": (70, 110, 380, 645),
            "round": (80, 125, 1395, 1555),
        },
    }

    # Current positions
    CURRENT_UI = UI_POSITIONS.get(SCREEN_RES, UI_POSITIONS[(1920, 1080)])

    # Bloon types
    BLOON_TYPES = [
        "red",
        "blue",
        "green",
        "yellow",
        "pink",
        "black",
        "white",
        "lead",
        "camo",
    ]

    # Game rules
    MAX_UPGRADES = 7  # Total across paths
    MAX_TIER = 5  # Per path


settings = Settings()
