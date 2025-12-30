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
from utils.logger import logger
from config.settings import settings


class Controller:
    def __init__(self, Placement_detector):

        # pydirectinput
        pydirectinput.FAILSAFE = True
        pydirectinput.PAUSE = 0.1

        # Placement detection
        self.PD = Placement_detector

    def sell_monkey(self, y: int, x: int):
        """Sell monkey at (Y,X)"""
        pydirectinput.moveTo(x, y)
        pydirectinput.click()
        time.sleep(1)
        pydirectinput.press("backspace")

    def place_monkey(self, name: str, y: int, x: int) -> bool:
        """Place monkey at (Y,X)"""
        try:
            if not self._validate_position(y, x):
                raise ValueError(f"Invalid position ({y}, {x})")

            key = get_monkey_key(name)

            pydirectinput.press(key)
            time.sleep(0.3)
            pydirectinput.moveTo(x, y)
            time.sleep(0.3)

            # Placement validation
            if self.PD.is_valid(y, x):
                pydirectinput.click()
                time.sleep(0.5)

                # Validate if monkey is placed correctly
                if not self.PD.verify_monkey_selected(y, x):
                    logger.warning(f"No monkey found at ({y}, {x})")
                    return False
                logger.info(f"Placed monkey: {name} at ({y}, {x})")
                return True
            else:
                # If invalid, cancel the whole operation
                logger.warning(f"Invalid spot at ({y}, {x}). Cancelling.")
                self.cancel()
                return False

        except ValueError as e:
            logger.warning(str(e))
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False

    def upgrade_monkey(self, monkey: str, path: int, y: int, x: int) -> bool:
        """Upgrade monkey at (Y,X). Returns success bool."""
        try:
            pydirectinput.moveTo(x, y)
            pydirectinput.click()
            time.sleep(0.5)

            # Upgrade
            key = "," if path == 1 else "." if path == 2 else "/"
            pydirectinput.press(key)
            time.sleep(0.3)

            # Cancel
            self.cancel()
            logger.info(f"Upgraded {monkey} path {path} at ({y}, {x})")
            return True

        except Exception as e:
            logger.error(f"Upgrade failed: {e}")
            self.cancel()  # Ensure clean exit
            return False

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

    def _validate_position(self, y, x):
        y1, x1, y2, x2 = settings.GAME_SIZE

        if y1 < y < y2 and x1 < x < x2:
            return True
        else:
            return False
