# @Author: Simmon
# @Date: 2025-11-20 23:34:13

"""
Mouse and Keyboard Controller
 - Control Mouse clicks
 - Control key presses
"""

import pydirectinput
import time
from utils.monkey_helpers import get_monkey_cost, get_monkey_key, get_upgrade_cost


class Controller:
    def __init__(self, Placement_detector):

        # pydirectinput
        pydirectinput.FAILSAFE = True
        pydirectinput.PAUSE = 0.1

        # Placement detection
        self.PD = Placement_detector

    def sell_monkey(self, y: int, x: int):
        pydirectinput.moveTo(x, y)
        pydirectinput.click()
        time.sleep(1)
        pydirectinput.press("backspace")

    def place_monkey(self, monkey: str, y: int, x: int) -> bool:
        """Place a monkey, checking for validity AFTER entering placement mode."""
        key = get_monkey_key(monkey)
        pydirectinput.press(key)
        time.sleep(0.3)

        # TODO: Location Validation

        pydirectinput.moveTo(x, y)
        time.sleep(0.3)

        # Placement validation
        if self.PD.is_valid(y, x):
            pydirectinput.click()
            print(f"Placed monkey: {monkey} at ({y}, {x})")
            return True
        else:
            # If invalid, cancel the whole operation
            print(f"Invalid spot at ({y}, {x}). Cancelling.")
            pydirectinput.press("esc")  # Cancel placement mode
            return False

    def upgrade_monkey(self, monkey: str, path: int, y: int, x: int):
        """Upgrade monkey"""
        key = "," if path == 1 else "." if path == 2 else "/"
        pydirectinput.moveTo(x, y)
        pydirectinput.click()
        time.sleep(1)
        pydirectinput.press(key)

        # Cancel the upgrade UI after upgrading
        self.cancel()

        print(f"Upgraded monkey: {monkey} | path: {path}")

    def unpause(self):
        pydirectinput.press("space")

    def spam_abilities(self):
        for i in range(10):
            pydirectinput.press(str(i))
            time.sleep(0.1)
        pydirectinput.press("-")
        time.sleep(0.1)
        pydirectinput.press("=")
        time.sleep(0.1)

    def cancel(self):
        # Only for when selected monkey, and want to UNSELECT it
        pydirectinput.press("esc")
