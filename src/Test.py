from vision.placement_detector import PlacementDetector
from game.game_state import GameState
import pyautogui
import pydirectinput
import time

if __name__ == "__main__":
    GAME = GameState()
    PC = PlacementDetector()

    while True:
        x, y = pyautogui.position()

        print(PC.is_valid(x, y))
        PC.capture_radius_rings(x, y)
        time.sleep(5)
