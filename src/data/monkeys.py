import json
from pathlib import Path
from config.settings import Settings

# Load once at import time
_DATA_PATH = Path(__file__).parent / "monkeys.json"
with open(_DATA_PATH) as f:
    DATA = json.load(f)
    MONKEYS = DATA["monkeys"]
    DIFFICULTY_MULTIPLIER = DATA["difficulty_multipliers"][Settings.DIFFICULTY]
