import json
from pathlib import Path
from config.settings import settings

# Load once at import time
_DATA_PATH = Path(__file__).parent / "monkeys.json"
with open(_DATA_PATH) as f:
    try:
        DATA = json.load(f)
    except json.JSONDecodeError:
        print("Invalid JSON")
    else:
        MONKEYS = DATA["monkeys"]
        DIFFICULTY_MULTIPLIER = DATA["difficulty_multipliers"][settings.DIFFICULTY]
    finally:
        f.close()
