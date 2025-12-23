# @Author: Simmon
# @Date: 2025-11-20 23:34:13

"""
Mouse and Keyboard Controller
 - Control Mouse clicks
 - Control key presses
"""

import pydirectinput
import json
import time


class Monkey_controller:
    def __init__(self, Placement_detector, difficulty="medium"):
        self.difficulty = difficulty

        # Data
        self.monkey_data = None
        self.difficulty_multiplier = None
        self.load_monkey_file()

        # pydirectinput
        pydirectinput.FAILSAFE = True
        pydirectinput.PAUSE = 0.1
        self.screen = pydirectinput.size()

        # Placement detection
        self.PD = Placement_detector

    def load_monkey_file(self):
        try:
            with open(r"X:\Dev\BTD6Bot\src\Action\Monkeys.json", "r") as file:

                data = json.load(file)
                self.monkey_data = data["monkeys"]
                self.difficulty_multiplier = data["difficulty_multipliers"][
                    self.difficulty.lower()
                ]
        except Exception as e:
            print(f"Error loading json file: {e}")

    def get_monkey_data(self, monkey):
        return self.monkey_data[monkey.lower()]

    def get_monkey_cost(self, monkey):
        return self.get_monkey_data(monkey)["b"] * self.difficulty_multiplier

    def get_monkey_key(self, monkey):
        return self.get_monkey_data(monkey)["k"].lower()

    def get_monkey_path(self, monkey_name, path):
        """
        return the path's upgrade costs in list[]
        In the case of paragon, return only cost
        """

        data = self.get_monkey_data(monkey_name)

        if path in (1, 2, 3):
            result = list(
                map(lambda x: x * self.difficulty_multiplier, data["u"][str(path)])
            )
            return result
        elif path == 4:  # paragon
            if "paragon" in data["u"]:
                return data["u"]["paragon"]["cost"] * self.difficulty_multiplier
            else:
                raise NameError("Monkey has no paragon!")
        else:
            raise ValueError("Invalid path")

    def sell_monkey(self, y, x):
        pydirectinput.moveTo(x, y)
        pydirectinput.click()
        time.sleep(1)
        pydirectinput.press("backspace")

    def place_monkey(self, monkey_name, y, x):
        """Place a monkey, checking for validity AFTER entering placement mode."""
        key = self.get_monkey_key(monkey_name)
        pydirectinput.press(key)
        time.sleep(0.3)

        pydirectinput.moveTo(x, y)
        time.sleep(0.1)  # Short pause for rendering

        if self.PD.is_valid(y, x):
            pydirectinput.click()
            print(f"Placed monkey: {monkey_name} at ({y}, {x})")
            return True
        else:
            # If invalid, cancel the whole operation
            print(f"Invalid spot at ({x}, {y}). Cancelling.")
            pydirectinput.press("esc")  # Cancel placement mode
            return False

    def upgrade_monkey(self, path, y, x):
        """Upgrade monkey"""
        key = "," if path == 1 else "." if path == 2 else "/"
        pydirectinput.moveTo(x, y)
        pydirectinput.click()
        time.sleep(1)
        pydirectinput.press(key)

        # Cancel the upgrade screen after upgrading
        self.cancel()

    def unpause(self):
        pydirectinput.press("space")

    def spam_abilities(self):
        for i in range(10):
            pydirectinput.press(str(i))
        pydirectinput.press("-")
        pydirectinput.press("=")

    def cancel(self):
        # Only for when selected monkey, and want to UNSELECT it
        pydirectinput.press("esc")

    def get_multiplier_cost(self, cost):
        return cost * self.difficulty_multiplier
