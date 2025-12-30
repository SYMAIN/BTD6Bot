from data.monkeys import MONKEYS, DIFFICULTY_MULTIPLIER
from utils.logger import logger


def get_monkey_cost(name: str) -> int:
    try:
        return int(MONKEYS[name]["b"] * DIFFICULTY_MULTIPLIER)
    except KeyError as e:
        logger.error(f"Unknown monkey: {e}")
        return 0
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 0


def get_monkey_key(name: str) -> str:
    try:
        return MONKEYS[name]["k"].lower()
    except KeyError as e:
        logger.error(f"Unknown monkey: {e}")
        return ""


def get_upgrade_cost(name: str, path: int, current_tier: int) -> int:
    """Cost to upgrade from current tier to next."""
    try:
        return MONKEYS[name]["u"][str(path)][current_tier] * DIFFICULTY_MULTIPLIER
    except KeyError as e:  # Use KeyError for dict lookups
        logger.error(f"Invalid data: {e}")
        return 0  # Or raise exception
    except IndexError as e:  # Use IndexError for list indices
        logger.error(f"Invalid tier {current_tier}: {e}")
        return 0
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 0


def get_monkey_data() -> dict:
    return MONKEYS


def get_monkey_names() -> list:
    return list(MONKEYS.keys())
