# @Author: Simmon
# @Date: 2025-12-13 14:45:36

class Game_State:
    def __init__(self, game_mode="medium"):
        self.round = 1
        self.total_round = 0
        self.health = 0
        self.gold = 0
        self.is_game_active = False
        self.set_mode(game_mode)
        self.monkey_location = [] # [[name,(x,y)]]
    
    def set_mode(self, game_mode):
        if game_mode == "easy":
            self.total_round = 40
            self.health = 200
            self.gold = 650
        elif game_mode == "medium":
            self.total_round = 60
            self.health = 150
            self.gold = 650
        elif game_mode == "hard":
            self.total_round = 80
            self.health = 100
            self.gold = 650
            self.round = 3
        
    def update_game_state(self, res):
        """Update game state from scan results"""
        try:
            # Update round
            if 'Round' in res and res['Round']:
                round_data = res['Round']
                if isinstance(round_data, dict) and round_data.get('current') is not None:
                    new_round = round_data['current']
                    old_round = self.round
                    
                    if new_round > old_round:
                        self.round = new_round
                        print(f"🎯 Round advanced to: {new_round}")
            
            # Update health
            if 'Health' in res:
                try:
                    health = int(res['Health']) if res['Health'] else 200
                    if health != self.health:
                        self.health = health
                except:
                    pass
            
            # Update gold
            if 'Gold' in res:
                try:
                    gold = res['Gold'] if isinstance(res['Gold'], (int, float)) else 0
                    if gold != self.gold:
                        self.gold = gold
                except:
                    pass
                    
        except Exception as e:
            print(f"Error updating game state: {e}")
    
    def _print_status(self):
        """Print current game status"""
        status_parts = []
        
        status_parts.append(f"Round: {self.round}")

        status_parts.append(f"Health: {self.health}")
        
        status_parts.append(f"Gold: 💰 ${self.gold}")
        
        if status_parts:
            print(f"📊 Status: {' | '.join(status_parts)}")