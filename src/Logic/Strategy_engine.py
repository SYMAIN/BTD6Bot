# @Author: Simmon
# @Date: 2025-11-21 11:43:28


"""
Create an instance strategy a bot may use base on map structure
Load various strategy

"""
from .strategies.base import Strategy
from .strategies.random_strat import RandomStrategy
from typing import Dict, Any
from typing import Optional


class StrategyEngine:
    def __init__(self, game, controller):
        self.current_strategy = None

        # Class Objects
        self.game = game
        self.controller = controller

        self.strategies: Dict[str, Strategy] = {}
        self.current_strategy: Optional[Strategy] = None
        self._register_strategies()

    def run(self):
        # Run strategy
        self.current_strategy.execute(self.game, self.controller)

    def _register_strategies(self):

        self.strategies["random"] = RandomStrategy()

    def select_strategy(self, strategy_name: str):
        if strategy_name in self.strategies:
            self.current_strategy = self.strategies[strategy_name]
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")
