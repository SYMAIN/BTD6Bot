# @Author: Simmon
# @Date: 2025-11-21 11:43:56

import mss
import numpy as np
import cv2
import pytesseract
import re
import time
import pyautogui


pytesseract.pytesseract.tesseract_cmd = r"X:\Tesseract\tesseract.exe"


class Screen_scanner:
    def __init__(self):
        # Resolution adjustments (+ In game scaling)
        self.screen = pyautogui.size()
        self.offset_x = 0
        self.offset_y = 0
        self._set_offset()

    def capture(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            frame = np.array(screenshot)
            return self.process_frame(frame)

    def process_frame(self, frame):
        regions = {
            "Health": frame[
                20 + self.offset_y : 60 + self.offset_y,
                140 + self.offset_x : 290 + self.offset_x,
            ],
            "Gold": frame[
                20 + self.offset_y : 60 + self.offset_y,
                370 - self.offset_x : 650,
            ],
            "Round": frame[
                30 + self.offset_y : 75 + self.offset_y,
                1400 + self.offset_x : 1555 + self.offset_x,
            ],
        }

        res = {}
        for k, v in regions.items():
            text = self.OCR_detection(k, v)

            if k == "Round":
                nums = re.findall(r"\d+", text)
                if len(nums) >= 2:
                    res[k] = {"current": int(nums[0]), "total": int(nums[1])}
                else:
                    res[k] = {"current": None, "total": None}
            elif k == "Gold":
                clean = text.replace("$", "").replace(",", "")
                try:
                    res[k] = int(clean) if clean.isdigit() else 0
                except:
                    res[k] = 0
            else:
                try:
                    res[k] = int(text) if text.isdigit() else 100
                except:
                    res[k] = 100

        return res

    def OCR_detection(self, name, frame):
        try:
            mask = self._preprocess(frame)

            # Debug: Save image
            debug_path = (
                rf"X:\Dev\BTD6Bot\Assets\Debug\{self.screen[1]}p\debug_{name}.png"
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
            white_mask = np.all(frame > 200, axis=2).astype(np.uint8) * 255

            # Alternative - look for bright pixels (if method 1 fails)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, bright_mask = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)

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

    def _set_offset(self):
        laptop_resolution = (1920, 1200)
        monitor_resolution = (1920, 1080)  # Main resolution
        # Found through trial and error (DO NOT TOUCH)
        if self.screen == laptop_resolution:
            self.offset_y = 50
            self.offset_x = -10
