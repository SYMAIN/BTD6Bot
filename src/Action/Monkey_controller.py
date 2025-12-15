# @Author: Simmon
# @Date: 2025-11-20 23:34:13

"""
Mouse and Keyboard Controller
 - Control Mouse clicks
 - Control key presses
"""

import pyautogui
import json
import time


class Monkey_controller:
    def __init__(self, difficulty):
        self.difficulty = difficulty

        # Data
        self.monkey_data = None
        self.difficulty_multiplier = None

        # pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        self.screen = pyautogui.size()

    def load_monkey_file(self, file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.monkey_data = data["monkeys"]
                self.difficulty_multiplier = data["difficulty_multipliers"][
                    self.difficulty.lower()
                ]
        except Exception as e:
            print(f"Error loading json file: {e}")

    def place_monkey(self, monkey, x, y):
        # Loading data
        monkey_data = self.monkey_data[monkey.lower()]
        key = self.get_monkey_key(monkey)
        cost = self.get_monkey_cost(monkey)

    def get_monkey_data(self, monkey):
        return self.monkey_data[monkey.lower()]

    def get_monkey_cost(self, monkey):
        return self.get_monkey_data(monkey)["b"]

    def get_monkey_key(self, monkey):
        return self.get_monkey_data(monkey)["k"]

    def get_monkey_path(self, monkey, path):
        data = self.get_monkey_data(monkey)

        if path in (1, 2, 3):
            return data["u"][str(path)]
        elif path == 4:  # paragon
            if "paragon" in data["u"]:
                return data["u"]["paragon"]
            else:
                raise NameError("Monkey has no paragon!")
        else:
            raise ValueError("Invalid path")

    def sell_monkey(self, x, y):
        pyautogui.moveTo(x, y)
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.press("backspace")

    def place_monkey(self, monkey_key, x, y):
        """Place a monkey in BTD6"""
        pyautogui.press(monkey_key)
        time.sleep(0.1)
        pyautogui.moveTo(x, y)
        pyautogui.click()

    def upgrade_monkey(self, path, x, y):
        """Upgrade monkey"""
        key = "," if path == "1" else "." if path == "2" else "/"
        pyautogui.moveTo(x, y)
        pyautogui.click()
        pyautogui.press(key)
        time.sleep(0.1)

    def unpause(self):
        pyautogui.press("space")

    def spam_abilities(self):
        for i in range(10):
            pyautogui.press(str(i))
        pyautogui.press("-")
        pyautogui.press("=")

    def cancel(self):
        # Only for when selected monkey, and want to UNSELECT it
        pyautogui.press("esc")
