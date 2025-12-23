# @Author: Simmon
# @Date: 2025-12-13 14:45:36

import pyautogui


class Game_State:
    def __init__(self, game_mode="medium"):
        self.round = 1
        self.total_round = 0
        self.health = 0
        self.gold = 0
        self.set_mode(game_mode)

        self.monkey_location = []
        # [{name, location (y,x), path}]
        # {name: dart Monkey, location: (123,456), path: (0,0,0)}
        self.is_game_active = False
        self.end_round = False

        self.game_size = self._init_screen_size()  # [y1, x1, y2, x2]

    def return_game_size(self):
        return self.game_size

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

        print(f"Screen Resolution: {screen_size}")
        return p1080 if screen_size == (1920, 1080) else p1200

    def set_mode(self, game_mode):
        if game_mode == "easy":
            self.total_round = 40
            self.health = 200
            self.gold = 650
        elif game_mode == "medium":
            self.total_round = 60
            self.health = 150
            self.gold = 650
        elif game_mode == "hard":
            self.total_round = 80
            self.health = 100
            self.gold = 650
            self.round = 3

    def update_game_state(self, res):
        """Update game state from scan results"""
        try:
            # Update round
            if "round" in res and res["round"]:
                round_data = res["round"]
                self.round = round_data["current"]

            # Update health
            if "health" in res:
                self.health = int(res["health"])

            # Update gold
            if "gold" in res:
                self.gold = int(res["gold"])

        except Exception as e:
            print(f"Error updating game state: {e}")

    # update monkey location with idx
    def update_monkey(self, new_data, idx):
        self.monkey_location[idx] = new_data

    def add_monkey(self, new_data):
        self.monkey_location.append(new_data)

    def _print_status(self):
        """Print current game status"""
        status_parts = []

        status_parts.append(f"Round: {self.round}")

        status_parts.append(f"Health: {self.health}")

        status_parts.append(f"Gold: 💰 ${self.gold}")

        if status_parts:
            print(f"📊 Status: {' | '.join(status_parts)}")
