# game/models.py
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Monkey:
    name: str
    location: Tuple[int, int]  # (y, x)
    path: Tuple[int, int, int]  # (top, middle, bottom)


@dataclass
class GameInfo:
    round_current: int
    round_total: int
    health: int
    gold: int


@dataclass
class UpgradeOption:
    name: str
    path: int  # 1,2,3
    cost: int
    location: Tuple[int, int]
    position_idx: int
