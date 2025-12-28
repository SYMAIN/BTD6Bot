# @Author: Simmon
# @Date: 2025-11-21 11:43:37
from data.game import UpgradeOption
from utils.monkey_helpers import get_upgrade_cost


class UpgradeManager:
    def __init__(self):
        pass

    def upgrade_main_path(self):
        pass

    def upgrade_defense_path(self):
        pass

    def upgrade_for_camo(self):
        pass

    def upgrade_for_lead(self):
        pass

    def get_upgrade_availability(self, monkeys: list) -> list:
        """
        Docstring for _get_upgrade_availability

        :param self: Description
        :param controller: type Class Object
        :param monkeys: Type Object -> [{Name, Location, Path}]


        Loop through all monkey placed
        Check prices and find one that is affordable
        Sort from most most to least

        If on path 5, there is no more upgrade left
        If two path is chosen, third path is closed (2,2,0)
        If one path is past 2nd upgrade, second path is stuck on 2nd upgrade (3,2,0), (4,2,0), (5,2,0), etc
        """

        upgrade_options = []
        max_total_upgrades = 7  # Any monkey, the maximum upgrades of all paths is 7 (not including paragon)
        for idx, monkey in enumerate(monkeys):
            name = monkey.name
            location = monkey.location
            current_path = monkey.path  # (0,0,0)

            available_paths = self._get_available_upgrades(current_path)

            for path in available_paths:
                next_upgrade_cost = get_upgrade_cost(name, path, current_path[path - 1])

                """
                
                # Path is path [top, middle, bottom]
                # Upgrade is upgrade [1,2,3,4,5]
                path costs [100,200,300,400,500]
                
                """

                option = UpgradeOption(name, path, next_upgrade_cost, location, idx)
                upgrade_options.append(option)

        sorted_upgrades = sorted(upgrade_options, key=lambda m: m.cost, reverse=True)
        return sorted_upgrades

    def _get_available_upgrades(self, current: tuple) -> list:
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

    def _is_valid_upgrade(self, upgrades: list) -> bool:
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
