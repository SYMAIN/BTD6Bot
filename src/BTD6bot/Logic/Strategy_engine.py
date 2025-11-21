# @Author: Simmon
# @Date: 2025-11-21 11:43:28
# @Last Modified by:   undefined
# @Last Modified time: 2025-11-21 11:43:28


"""
Create an instance strategy a bot may use base on map structure
Load various strategy
  
"""

class Strategy_engine:
    def __init__(self):
        self.strategies = []
        self.current_strategy = None
    
    def choose_strategy(self):
        pass

    def save_money(self):
        pass

    def get_tower_priority(self):
        pass

    def get_upgrade_priority(self):
        pass