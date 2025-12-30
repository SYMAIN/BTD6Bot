# @Author: Simmon
# @Date: 2025-11-21 11:43:56

from config.settings import settings
from data.game import GameInfo
import time

"""
At the beginning of each round, use all abilities
- Make it easier
"""


class Bot:
    def __init__(self, scanner, game_state, strategy_engine, pause_event):
        self.scanner = scanner
        self.game_state = game_state
        self.strategy_engine = strategy_engine

        # Control flags
        self.running = True  # Allows external control
        self.pause_event = pause_event

        # Timing control
        self.last_capture_time = 0
        self.last_strategy_time = 0

        # Statistics
        self.capture_count = 0
        self.start_time = time.time()

    def run(self):
        """Main bot loop - can be stopped by setting self.running = False"""
        print("Bot main loop started")

        self.strategy_engine.select_strategy("random")  # First strategy

        try:
            while self.running:
                self.pause_event.wait()

                # Screen Capture
                current_time = time.time()
                if current_time - self.last_capture_time >= settings.CAPTURE_INTERVAL:

                    self.screen_capture()
                    self.strategy_engine.run()

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

            def _to_int(val, default=0):
                try:
                    if val is None:
                        return default
                    return int(val)
                except (ValueError, TypeError):
                    return default

            _res = GameInfo(
                _to_int(res.get("round", {}).get("current")),
                _to_int(res.get("round", {}).get("total")),
                _to_int(res.get("health")),
                _to_int(res.get("gold")),
            )

            # Log if scanner returned unexpected values
            if any(
                v is None
                for v in [
                    res.get("health"),
                    res.get("gold"),
                    res.get("round", {}).get("current"),
                    res.get("round", {}).get("total"),
                ]
            ):
                print(
                    "Warning: Scanner returned missing or invalid numeric fields; using defaults where necessary."
                )

            # Update game state
            self.game_state.update(_res)

            # Print current state
            self.game_state.print_status()

        except Exception as e:
            print(f"Error in screen_capture: {e}")
