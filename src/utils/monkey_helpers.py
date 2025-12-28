from data.monkeys import MONKEYS, DIFFICULTY_MULTIPLIER


def get_monkey_cost(name: str) -> int:
    return int(MONKEYS[name]["b"] * DIFFICULTY_MULTIPLIER)


def get_monkey_key(name: str) -> str:
    return MONKEYS[name]["k"].lower()


def get_upgrade_cost(name: str, path: int, current_tier: int) -> int:
    """Cost to upgrade from current tier to next."""
    return MONKEYS[name]["u"][str(path)][current_tier] * DIFFICULTY_MULTIPLIER


def get_monkey_data() -> dict:
    return MONKEYS


def get_monkey_names() -> list:
    return list(MONKEYS.keys())
