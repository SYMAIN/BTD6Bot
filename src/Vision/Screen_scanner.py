# @Author: Simmon
# @Date: 2025-11-21 11:43:56

import mss
import numpy as np
import cv2
import pytesseract
import re
import time
import pyautogui
from config.settings import Settings

pytesseract.pytesseract.tesseract_cmd = Settings.TESSERACT_PATH


class ScreenScanner:
    def __init__(self):
        pass

    def capture(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            frame = np.array(screenshot)
            return self.process_frame(frame)

    def process_frame(self, frame) -> dict:
        health = Settings.CURRENT_UI["health"]
        gold = Settings.CURRENT_UI["gold"]
        _round = Settings.CURRENT_UI["round"]

        regions = {
            "health": frame[health[0] : health[1], health[2] : health[3]],
            "gold": frame[gold[0] : gold[1], gold[2] : gold[3]],
            "round": frame[_round[0] : _round[1], _round[2] : _round[3]],
        }

        res = {}
        for k, v in regions.items():
            text = self._OCR_detection(k, v)

            if k == "round":
                nums = re.findall(r"\d+", text)
                if len(nums) >= 2:
                    res[k] = {"current": int(nums[0]), "total": int(nums[1])}
                else:
                    res[k] = {"current": None, "total": None}
            elif k == "gold":
                clean = text.replace("$", "").replace(",", "")
                res[k] = int(clean)
            else:  # Health
                res[k] = int(text)

        return res

    def _OCR_detection(self, name: str, frame) -> str:
        try:
            mask = self._preprocess(frame)

            # Debug: Save image
            debug_path = (
                rf"{Settings.DEBUG_DIR}\{Settings.SCREEN_RES[1]}p\debug_{name}.png"
            )
            cv2.imwrite(debug_path, mask)

            config = "--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789,/"

            text = pytesseract.image_to_string(mask, config=config).strip()

            print(f"[{time.strftime('%H:%M:%S')}] {name}: {text}")
            return text

        except Exception as e:
            print(f"Error processing {name}: {e}")
            return ""

    def _preprocess(self, frame):
        try:
            # Create a mask where pixels are mostly white (all channels > 200)
            white_mask = np.all(frame > 240, axis=2).astype(np.uint8) * 255

            # Alternative - look for bright pixels (if method 1 fails)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, bright_mask = cv2.threshold(gray, 255, 255, cv2.THRESH_BINARY)

            combined = cv2.bitwise_or(white_mask, bright_mask)
            if frame.shape[0] < 50:  # If ROI height is less than 50px
                combined = cv2.resize(
                    combined, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC
                )

            # Invert for OCR
            result = cv2.bitwise_not(combined)
            return result

        except Exception as e:
            print(f"Preprocessing error: {e}")
            return np.zeros((50, 200), dtype=np.uint8)
