# @Author: Simmon
# @Date: 2025-11-21 11:43:56

from Vision.Screen_scanner import Screen_scanner
from Action.Monkey_controller import Monkey_controller
from Logic.Strategy_engine import Strategy_engine
from Vision.Placement_detector import Placement_detector
from Game import Game_State
import time

"""
At the beginning of each round, use all abilities
- Make it easier
"""


class Bot:
    def __init__(self, pause_event):
        self.scanner = Screen_scanner()
        self.game = Game_State()
        self.PD = Placement_detector(*self.game.return_game_size())
        self.MC = Monkey_controller(self.PD, difficulty="hard")
        self.SE = Strategy_engine(self.game, self.MC)

        # Control flags
        self.running = True  # Allows external control
        self.pause_event = pause_event

        # Timing control
        self.last_capture_time = 0
        self.capture_interval = 5.0
        self.last_strategy_time = 0

        # Statistics
        self.capture_count = 0
        self.start_time = time.time()
        self.end_round = False

    def run(self):
        """Main bot loop - can be stopped by setting self.running = False"""
        print("Bot main loop started")

        self.SE.select_strategy(1)  # First strategy

        try:
            while self.running:
                self.pause_event.wait()

                # Screen Capture
                current_time = time.time()
                if current_time - self.last_capture_time >= self.capture_interval:

                    self.screen_capture()
                    self.SE.run()

                    self.last_capture_time = current_time
                    self.capture_count += 1

                # Small sleep to prevent CPU hogging
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("Bot interrupted by keyboard")
        except Exception as e:
            print(f"Bot error: {e}")
            import traceback

            traceback.print_exc()
        finally:
            print(f"Bot stopped. Captured {self.capture_count} screens.")

    def screen_capture(self):
        """Capture and process screen"""
        try:
            timestamp = time.strftime("%H:%M:%S")
            print(f"\n[{timestamp}] Capture #{self.capture_count + 1}")

            # Capture and get results
            res = self.scanner.capture()

            if not res:
                print("No results from scanner")
                return

            # # Print raw results for debugging (less verbose)
            # if self.capture_count % 10 == 0:  # Only every 10th capture
            #     print(f"Raw: {res}")

            # Update game state
            self.game.update_game_state(res)

            # Print current state
            self.game._print_status()

        except Exception as e:
            print(f"Error in screen_capture: {e}")

    def get_stats(self):
        """Get bot statistics"""
        elapsed = time.time() - self.start_time
        return {
            "captures": self.capture_count,
            "runtime": elapsed,
            "avg_interval": (
                elapsed / self.capture_count if self.capture_count > 0 else 0
            ),
            "round": self.game.round if hasattr(self.game, "round") else 0,
            "health": self.game.health if hasattr(self.game, "health") else 0,
            "gold": self.game.gold if hasattr(self.game, "gold") else 0,
        }
