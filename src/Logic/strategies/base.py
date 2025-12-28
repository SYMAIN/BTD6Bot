from abc import ABC, abstractmethod
from typing import Dict, Any
from ..upgrade_manager import UpgradeManager


class Strategy(ABC):
    """Base class for all strategies."""

    def __init__(self):
        self.UM = UpgradeManager()

    @abstractmethod
    def execute(self, game_state: Dict[str, Any], controller) -> None:
        """Execute the strategy."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return strategy name."""
        pass
