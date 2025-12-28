# config/settings.py
import os
from dataclasses import dataclass
from pathlib import Path
import pyautogui
from . import constants


@dataclass
class Settings:
    # Screen
    WIDTH, HEIGHT = pyautogui.size()
    SCREEN_RES = (WIDTH, HEIGHT)

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

    @property
    def CURRENT_UI(self):
        return constants.UI_POSITIONS.get(
            pyautogui.size(), constants.UI_POSITIONS[(1920, 1080)]
        )

    # Game size, placeable area
    @property
    def GAME_SIZE(self):
        """Calculate game bounds based on resolution. [y1, x1, y2, x2]"""
        if self.SCREEN_RES == (1920, 1080):
            return [
                constants.IN_GAME_OFFSET,
                constants.IN_GAME_OFFSET + constants.BORDER_1080_X_OFFSET,
                self.HEIGHT - constants.IN_GAME_OFFSET,
                self.WIDTH - constants.IN_GAME_OFFSET - constants.MONKEY_MENU_X_OFFSET,
            ]
        else:  # 1200p
            return [
                constants.IN_GAME_OFFSET + constants.BORDER_1200_Y_OFFSET,
                constants.IN_GAME_OFFSET,
                self.HEIGHT - constants.IN_GAME_OFFSET - constants.BORDER_1200_Y_OFFSET,
                self.WIDTH - constants.IN_GAME_OFFSET - constants.MONKEY_MENU_X_OFFSET,
            ]


settings = Settings()
