from .base import Strategy
from utils.monkey_helpers import (
    get_monkey_cost,
    get_monkey_key,
    get_upgrade_cost,
    get_monkey_names,
)
from data.game import UpgradeOption, Monkey
import random
from config.settings import settings


class RandomStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.name = "random"

    def get_name(self):
        return self.name

    def execute(self, game_state, controller):
        """
        OPtions:
        Place monkey
        Upgrade

        Plan:
        If an upgrade is available -> Upgrade
        Else place new monkey -> Place

        What Monkey??
        Random
        """
        upgrade_options = self.UM.get_upgrade_availability(game_state.monkey_location)
        current_gold = game_state.gold

        # Filter affordable upgrades first
        affordable_options = [
            opt for opt in upgrade_options if opt.cost <= current_gold
        ]

        if affordable_options:
            # Pick random affordable upgrade
            option = random.choice(affordable_options)

            # Upgrade
            controller.upgrade_monkey(
                option.name, option.path, option.location[0], option.location[1]
            )

            # Update game state
            monkey = game_state.monkey_location[option.position_idx]
            new_path = list(monkey.path)
            new_path[option.path - 1] += 1  # Path is 1,2,3 → index 0,1,2

            updated_monkey = Monkey(
                name=option.name, location=option.location, path=tuple(new_path)
            )
            game_state.update_monkey(updated_monkey, option.position_idx)

        else:
            # Place new monkey
            monkey_name, location = self._random_monkey_location()
            cost = get_monkey_cost(monkey_name)

            if current_gold >= cost and controller.place_monkey(
                monkey_name, location[0], location[1]
            ):
                new_monkey = Monkey(name=monkey_name, location=location, path=(0, 0, 0))
                game_state.add_monkey(new_monkey)

    def _random_monkey_location(self):

        # TODO: Place hero
        game_size = settings.GAME_SIZE
        while True:
            monkey_name = random.choice(get_monkey_names())
            if monkey_name != "heroes":
                break

        while True:
            x = random.randrange(game_size[1], game_size[3])  # x within width
            y = random.randrange(game_size[0], game_size[2])  # y within height
            print(f"Random position: x{x}, y{y}")
            return monkey_name, (y, x)
