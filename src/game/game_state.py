# @Author: Simmon
# @Date: 2025-12-13 14:45:36

from config.settings import settings
from data.game import GameInfo, Monkey
import pyautogui
import json


class GameState:
    def __init__(self, game_mode="medium"):

        # In game
        self.monkey_location = []  # Monkey object
        self.round = 1
        self.total_round = 0
        self.health = 0
        self.gold = 0
        self.game_mode = game_mode

    def to_info(self) -> GameInfo:
        """Export snapshot."""
        return GameInfo(
            round_current=self.round,
            round_total=self.total_round,
            health=self.health,
            gold=self.gold,
        )

    def update(self, data: GameInfo):
        """Update game state from scan results"""
        try:
            # Update round
            self.round = int(data.round_current)
            self.total_round = int(data.round_total)

            # Update health
            self.health = int(data.health)

            # Update gold
            self.gold = int(data.gold)

        except Exception as e:
            print(f"Error updating game state: {e}")

    # update monkey location with idx
    def update_monkey(self, data: Monkey, idx):
        self.monkey_location[idx] = data

    def add_monkey(self, data: Monkey):
        self.monkey_location.append(data)

    def print_status(self):
        """Print current game status"""
        status_parts = []

        status_parts.append(f"Round: {self.round}")

        status_parts.append(f"Health: {self.health}")

        status_parts.append(f"Gold: 💰 ${self.gold}")

        if status_parts:
            print(f"📊 Status: {' | '.join(status_parts)}")
