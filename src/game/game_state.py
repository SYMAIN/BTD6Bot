# @Author: Simmon
# @Date: 2025-12-13 14:45:36

from config.settings import Settings
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

        self.game_size = None

        self.init()

    def init(self):
        self._init_screen_size()
        self.set_mode()

    def get_game_size(self):
        return self.game_size

    def to_info(self) -> GameInfo:
        """Export snapshot."""
        return GameInfo(
            round_current=self.round,
            round_total=self.total_round,
            health=self.health,
            gold=self.gold,
        )

    def _init_screen_size(self):
        w, h = screen_size = pyautogui.size()
        game_offset = 100
        monkey_menu_offset_x = 280

        # 1080p
        border_1080_x = 25  # pixels
        p1080 = [
            game_offset,  # y1 = 100
            game_offset + border_1080_x,  # x1 = 100 + 25 = 125
            h - game_offset,  # y2 = 1080 - 100 = 980
            w - game_offset - monkey_menu_offset_x,  # x2 = 1920 - 100 - 280 = 1540
        ]  # [y1, x1, y2, x2]

        # 1200p
        border_1200_y = 45
        p1200 = [
            game_offset + border_1200_y,  # y1 = 100 + 45 = 145
            game_offset,  # x1 = 100
            h - game_offset - border_1200_y,  # y2 = 1200 - 100 - 45 = 1055
            w - game_offset - monkey_menu_offset_x,  # x2 = 1920 - 100 - 280 = 1540
        ]  # [y1, x1, y2, x2]

        self.game_size = p1080 if screen_size == (1920, 1080) else p1200

    # TODO: Not sure if we need it
    def set_mode(self):
        if self.game_mode == "easy":
            self.total_round = 40
            self.health = 200
            self.gold = 650
        elif self.game_mode == "medium":
            self.total_round = 60
            self.health = 150
            self.gold = 650
        elif self.game_mode == "hard":
            self.total_round = 80
            self.health = 100
            self.gold = 650
            self.round = 3

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
