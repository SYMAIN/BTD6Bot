import pyautogui
from PIL import ImageGrab
import os
import datetime

"""
Gather information about the screen
 - Blood Path
 - Gold
 - Health
 - Round

"""
class Screen_scanner:
  def __init__(self):
    pass

  def take_screenshot(self):
    # Capture the entire screen
    screenshot = ImageGrab.grab()

    # Generate filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/fullscreen_{timestamp}.png"

    # Save the screenshot
    screenshot.save(filename, "PNG")
    print(f"Screenshot saved as: {filename}")

    return screenshot
  
  