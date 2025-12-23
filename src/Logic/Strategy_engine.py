# @Author: Simmon
# @Date: 2025-11-21 11:43:28


"""
Create an instance strategy a bot may use base on map structure
Load various strategy

"""
import random


class Strategy_engine:
    def __init__(self, game, controller):
        self.current_strategy = None
        self.strategies = ["random"]

        # Class Objects
        self.game = game
        self.controller = controller

    def run(self):
        # Run strategy
        if self.current_strategy == "random":
            self._random()

    def select_strategy(self, strategyN):
        self.current_strategy = self.strategies[strategyN - 1]

    def _random(self):
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
        upgrade_options = self._get_upgrade_availability(
            self.controller.get_monkey_path, self.game.monkey_location
        )

        """upgrade_option  = {
            "monkey": name,
            "path": path,  # 1=top, 2=middle, 3=bottom
            "cost": next_upgrade_cost,
            "location": location,
            }
        """
        current_gold = self.game.gold

        option = None
        for _option in upgrade_options:
            if current_gold >= _option["cost"]:
                option = _option
                break
            print(f"options: {_option} ")
        print("\n\n")

        # Upgrade path
        if option is not None:
            # Upgrade
            location = option["location"]
            path = option["path"]
            self.controller.upgrade_monkey(path, location[0], location[1])  # (y,x)
            # TODO: Fix upgrade; only upgrades top path
            # updating saved game data
            idx = option["position_idx"]
            new_data = self.game.monkey_location[idx].copy()
            new_path = new_data["path"]
            if path == 1:
                new_path = (new_path[0] + 1, new_path[1], new_path[2])
            elif path == 2:
                new_path = (new_path[0], new_path[1] + 1, new_path[2])
            elif path == 3:
                new_path = (new_path[0], new_path[1], new_path[2] + 1)

            new_data["path"] = new_path
            self.game.update_monkey(new_data, idx)

            print(f"Upgraded monkey: {new_data["name"]} | path: {new_path}")
        else:
            # Place monkey
            monkey_name, location = self._random_monkey_location()
            cost = self.controller.get_monkey_cost(monkey_name)

            if current_gold >= cost:
                if self.controller.place_monkey(monkey_name, location[0], location[1]):

                    # Save monkey location
                    new_data = {
                        "name": monkey_name,
                        "location": location,  # (y,x)
                        "path": (0, 0, 0),
                    }
                    self.game.add_monkey(new_data)

    def _random_monkey_location(self):
        game_size = self.game.return_game_size()
        while True:
            monkey_name = random.choice(list(self.controller.monkey_data.keys()))
            if monkey_name != "heroes":
                break

        while True:
            x = random.randrange(game_size[1], game_size[3])  # x within width
            y = random.randrange(game_size[0], game_size[2])  # y within height
            print(f"Random position: x{x}, y{y}")
            return monkey_name, (y, x)

    def determine_monkey_location(self):
        pass

    def _get_upgrade_availability(self, monkey_path_cost, monkeys):
        """
        Docstring for _get_upgrade_availability

        :param self: Description
        :param controller: type Class Object
        :param monkeys: Type Object -> [{Name, Location, Path}]


        Loop through all monkey placed
        Check prices and find one that is affordable
        Sort from most expansive to least

        If on path 5, there is no more upgrade left
        If two path is chosen, third path is closed (2,2,0)
        If one path is past 2nd upgrade, second path is stuck on 2nd upgrade (3,2,0), (4,2,0), (5,2,0), etc
        """

        upgrade_options = []
        max_total_upgrades = 7  # Any monkey, the maximum upgrades of all paths is 7 (not including paragon)
        for idx, monkey in enumerate(monkeys):
            name = monkey["name"]
            location = monkey["location"]
            current_path = monkey["path"]  # (0,0,0)

            available_paths = self._get_available_upgrades(current_path)

            for path in available_paths:
                path_costs = monkey_path_cost(name, path)  # [100,200,300,400,500]

                """
                
                # Path is path [top, middle, bottom]
                # Upgrade is upgrade [1,2,3,4,5]
                path costs [100,200,300,400,500]
                next_upgrade_tier : (3,2,0) of path 1 -> 3
                next_upgrade_cost : upgrade from 3 to 4 cost -> $400
                
                """
                next_upgrade_tier = current_path[path - 1]  # ex. (3,2,0) of path 1 -> 3

                next_upgrade_cost = path_costs[
                    next_upgrade_tier
                ]  # ex. upgrade from 3 to 4 cost

                upgrade_options.append(
                    {
                        "monkey": name,
                        "path": path,  # 1=top, 2=middle, 3=bottom
                        "cost": next_upgrade_cost,
                        "location": location,
                        "position_idx": idx,
                    }
                )
        sorted_upgrades = sorted(upgrade_options, key=lambda m: m["cost"])
        return sorted_upgrades

    def _get_available_upgrades(self, current):
        """current = [3, 2, 0]"""
        current = list(current)  # Convert tuple to list
        available = []

        # Check each path
        for i in range(3):
            if current[i] >= 5:
                continue  # Max tier reached

            # Check if we can upgrade this path
            temp = current.copy()
            temp[i] += 1

            if self._is_valid_upgrade(temp):
                available.append(i + 1)  # path index 0,1,2 is available

        return available

    def _is_valid_upgrade(self, upgrades):
        # upgrades = [top, middle, bottom] like [3, 2, 0]

        if sum(upgrades) > 7:
            return False

        # Rule 1: At least one is 0 (no investment)
        if upgrades.count(0) == 0:
            return False

        # Rule 2: Only one path can be >= 3
        three_or_more = sum(1 for x in upgrades if x >= 3)
        if three_or_more > 1:
            return False

        # Rule 3: If one path is >= 3, others max at 2
        if any(x >= 3 for x in upgrades):
            for x in upgrades:
                if x != 0 and x < 3:
                    if x > 2:
                        return False

        # Rule 4: Max tier is 5
        if any(x > 5 for x in upgrades):
            return False

        return True
