# @Author: Simmon
# @Date: 2025-11-20 23:34:13

"""
Mouse and Keyboard Controller
 - Control Mouse clicks
 - Control key presses
"""

import pyautogui
import json

class Monkey_controller:
  def __init__(self, difficulty):
    self.difficulty = difficulty

    # Data
    self.monkey_data = None
    self.difficulty_multiplier = None

  def load_monkey_file(self, file_name):
    try:
      with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
        self.monkey_data = data["monkeys"]
        self.difficulty_multiplier = data["difficulty_multipliers"][self.difficulty.lower()]
    except Exception as e:
      print(f"Error loading json file: {e}")

  def place_monkey(self, monkey, x, y):
    # Loading data
    monkey_data = self.monkey_data[monkey.lower()]
    key = self.get_monkey_key(monkey)
    cost = self.get_monkey_cost(monkey)

  def get_monkey_data(self, monkey):
      return self.monkey_data[monkey.lower()]

  def get_monkey_cost(self, monkey):
      return self.get_monkey_data(monkey)["b"]

  def get_monkey_key(self, monkey):
      return self.get_monkey_data(monkey)["k"]

  def get_monkey_path(self, monkey, path):
      data = self.get_monkey_data(monkey)

      if path in (1, 2, 3):
          return data["u"][str(path)]
      elif path == 4:  # paragon
          if "paragon" in data["u"]:
            return data["u"]["paragon"]
          else:
             raise NameError("Monkey has no paragon!")
      else:
          raise ValueError("Invalid path")


  def press_key(self, key):
    pass

  def click(self, x, y):
    pass
