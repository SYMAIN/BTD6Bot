# @Author: Simmon
# @Date: 2025-11-21 11:43:56

from Vision.Screen_scanner import Screen_scanner
from Game import Game_State
import keyboard
import threading
import time

class Bot:
    def __init__(self):
        self.running = False
        self.scanner = Screen_scanner(use_threading=True)
        self.game = Game_State()
        
        # Set up hotkeys
        keyboard.add_hotkey('f2', self.start_process)
        keyboard.add_hotkey('f3', self.stop_process)
        
        # Timing control
        self.last_capture_time = 0
        self.capture_interval = 1.0  # Capture every 1 second
    
    def run(self):
        print("Bot started. Press F2 to start scanning, F3 to stop.")
        print("Hotkeys:")
        print("  F2 - Start scanning")
        print("  F3 - Stop scanning")
        print("  Ctrl+C - Exit program")
        
        try:
            while True:
                if self.running:
                    current_time = time.time()
                    if current_time - self.last_capture_time >= self.capture_interval:
                        self.screen_capture()
                        self.last_capture_time = current_time
                
                # Small sleep to prevent CPU hogging
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\nExiting...")
            self.stop_process()
    
    def stop_process(self):
        if self.running:
            self.running = False
            print("Bot stopped")
    
    def start_process(self):
        if not self.running:
            self.running = True
            print("Bot started scanning")
    
    def screen_capture(self):
        """Capture and process screen"""
        try:
            print(f"\n[{time.strftime('%H:%M:%S')}] Capturing screen...")
            
            # Capture and get results
            res = self.scanner.capture()
            
            if not res:
                print("No results from scanner")
                return
            
            # Debug: Print all results
            print(f"Raw results: {res}")
            
            # Update game state
            self._update_game_state(res)
            
            # Print current state
            self._print_status()
            
        except Exception as e:
            print(f"Error in screen_capture: {e}")
            import traceback
            traceback.print_exc()
    
    def _update_game_state(self, res):
        """Update game state from scan results"""
        try:
            # Update round
            if 'Round' in res and res['Round']:
                round_data = res['Round']
                if (isinstance(round_data, dict) and 
                    round_data.get('current') is not None):
                    
                    new_round = round_data['current']
                    if hasattr(self.game, 'round'):
                        old_round = getattr(self.game, 'round', 0)
                        
                        # Only update if round advanced
                        if new_round > old_round:
                            self.game.round = new_round
                            print(f"Round advanced to: {new_round}")
                            
                            # Update other stats on round change
                            self._update_round_stats(res)
                    else:
                        self.game.round = new_round
            
            # Update health
            if 'Health' in res:
                try:
                    health = int(res['Health']) if res['Health'] else 100
                    self.game.health = health
                except (ValueError, TypeError):
                    pass
            
            # Update gold (continuous, not just on round change)
            if 'Gold' in res:
                try:
                    gold = res['Gold'] if isinstance(res['Gold'], (int, float)) else 0
                    self.game.gold = gold
                except (ValueError, TypeError):
                    pass
                    
        except Exception as e:
            print(f"Error updating game state: {e}")
    
    def _update_round_stats(self, res):
        """Update stats that should only update on round change"""
        pass
    
    def _print_status(self):
        """Print current game status"""
        status_parts = []
        
        if hasattr(self.game, 'round') and self.game.round:
            status_parts.append(f"Round: {self.game.round}")
        
        if hasattr(self.game, 'health') and self.game.health is not None:
            status_parts.append(f"Health: {self.game.health}")
        
        if hasattr(self.game, 'gold') and self.game.gold is not None:
            status_parts.append(f"Gold: ${self.game.gold}")
        
        if status_parts:
            print(f"Current: {' | '.join(status_parts)}")