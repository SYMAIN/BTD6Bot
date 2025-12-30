# config/settings.py
import os
from dataclasses import dataclass


# Game rules
MAX_UPGRADES = 7  # Total across paths
MAX_TIER = 5  # Per path

# Screen UI Location
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

# UI Offsets
# Offset from the border to remove clipping and invalid placement
IN_GAME_OFFSET = 100
MONKEY_MENU_X_OFFSET = 280  # pixel Width of monkey menu
BORDER_1080_X_OFFSET = 25  # pixels
BORDER_1200_Y_OFFSET = 45


# Placement Detection
PLACEMENT_DETECTION_RADII = [
    75,
    100,
    125,
    150,
    175,
    200,
    225,
    250,
    275,
    300,
    325,
]  # Pixel radii for placement validation

RADIUS_SAMPLE_SIZE = 50
# Exponent controlling sampling scaling: smaller radii get more samples.
RADIUS_SAMPLE_EXPONENT = 1.5
# Separate exponent for weighting rings (how much more influence small radii have)
RADIUS_WEIGHT_EXPONENT = 2.0
# Maximum multiplier for samples (allows denser sampling for tiny radii)
MAX_SAMPLE_MULTIPLIER = 6
# If the N smallest rings have a combined invalid fraction below this
# threshold, consider the placement valid immediately.
SMALL_RADIUS_ACCEPT_COUNT = 2
SMALL_RADIUS_ACCEPT_THRESHOLD = 0.05

VALID_SCORE = 0.1

MONKEY_EXIST_MENU_COLOR = [
    128,
    74,
    36,
]  # When a monkey is pressed, a upgrade menu pops out. This color will appear in the thousands.
