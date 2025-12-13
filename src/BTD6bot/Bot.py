# @Author: Simmon
# @Date: 2025-11-21 11:43:56

from Vision.Screen_scanner import Screen_scanner
import keyboard
import threading
import time

class Bot:
    def __init__(self):
        self.running = False
        self.scanner = Screen_scanner()
        # Set up hotkeys in main thread
        keyboard.add_hotkey('f2', self.start_process)
        keyboard.add_hotkey('f3', self.stop_process)
    
    def run(self):
        print("Bot started. Press F2 to start scanning, F3 to stop.")
        # Main thread now just waits
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_process()
    
    def stop_process(self):
        if self.running:
            self.running = False
            self.scanner.stop()
            print("Bot stopped")
    
    def start_process(self):
        if not self.running:
            self.running = True
            self.scanner.start()
            print("Bot started scanning")