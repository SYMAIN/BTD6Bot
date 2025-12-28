from Vision.Placement_detector import Placement_detector
from Game.Game import Game_State
import pyautogui
import pydirectinput
import time

if __name__ == "__main__":
    GAME = Game_State()
    bounds = GAME.return_game_size()
    PC = Placement_detector(*GAME.return_game_size())

    while True:
        # x, y = pyautogui.position()

        # print(PC.is_valid(x, y))

        time.sleep(1)
