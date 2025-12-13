# @Author: Simmon
# @Date: 2025-12-13 14:45:36

class Game_State:
    def __init__(self):
        self.round = 0
        self.health = 100
        self.gold = 0
        self.wave = 1
        self.is_game_active = False
        
    def reset(self):
        """Reset game state"""
        self.round = 0
        self.health = 100
        self.gold = 0
        self.wave = 1
        self.is_game_active = False
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'round': self.round,
            'health': self.health,
            'gold': self.gold,
            'wave': self.wave,
            'is_game_active': self.is_game_active
        }
    
    def __str__(self):
        return (f"Round: {self.round}, Health: {self.health}, "
                f"Gold: ${self.gold}, Wave: {self.wave}")