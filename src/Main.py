# @Author: Simmon
# @Date: 2025-11-21 11:44:01

from Bot import Bot as BotClass  # Rename to avoid conflict
import keyboard
import time


class Main:
    def __init__(self):
        self.bot_instance = None  # Track the bot instance
        self.running = False

        # Set up hotkeys
        keyboard.add_hotkey("f2", self.start_process)
        keyboard.add_hotkey("f3", self.stop_process)
        keyboard.add_hotkey("ctrl+q", self.exit_program)
        keyboard.add_hotkey("f1", self.key_instruction)

    def run(self):
        """Main loop - just wait for hotkeys"""
        self.key_instruction()
        print("\nWaiting for hotkeys...")

        try:
            # Keep the program running
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.exit_program()

    def key_instruction(self):
        print("\n" + "=" * 50)
        print("BTD6 Bot Controller")
        print("=" * 50)
        print("Hotkeys:")
        print("  F1 - Show this help")
        print("  F2 - Start bot")
        print("  F3 - Stop bot")
        print("  Ctrl+Q - Exit program")
        print("=" * 50)

    def start_process(self):
        """Start the bot"""
        if self.running:
            print("Bot is already running!")
            return

        print("\nStarting bot...")
        self.running = True

        # Create and start bot instance
        self.bot_instance = BotClass()

        # Start bot in a separate thread so we don't block hotkeys
        import threading

        self.bot_thread = threading.Thread(target=self._run_bot)
        self.bot_thread.daemon = True  # Thread will exit when main program exits
        self.bot_thread.start()

        print("Bot started!")

    def _run_bot(self):
        """Internal method to run the bot"""
        try:
            self.bot_instance.run()
        except Exception as e:
            print(f"Bot crashed: {e}")
            import traceback

            traceback.print_exc()
            self.running = False

    def stop_process(self):
        """Stop the bot"""
        if not self.running:
            print("Bot is not running!")
            return

        print("\nStopping bot...")
        self.running = False

        # Signal the bot to stop
        if hasattr(self.bot_instance, "running"):
            self.bot_instance.running = False

        # Wait a bit for clean shutdown
        time.sleep(0.5)
        print("Bot stopped.")

    def exit_program(self):
        """Exit the program cleanly"""
        print("\n" + "=" * 50)
        print("Exiting program...")

        # Stop bot if running
        if self.running:
            self.stop_process()

        # Additional cleanup
        print("Cleaning up...")

        # Close any OpenCV windows
        try:
            import cv2

            cv2.destroyAllWindows()
        except:
            pass

        print("Goodbye!")

        # Exit the program
        import sys

        sys.exit(0)


if __name__ == "__main__":
    main = Main()
    main.run()
