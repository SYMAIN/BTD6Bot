# @Author: Simmon
# @Date: 2025-11-21 11:43:50

import mss
import time
import threading
import numpy as np
import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'X:\Tesseract\tesseract.exe'

class Screen_scanner:
    def __init__(self, use_threading=True):
        self.use_threading = use_threading
        self.latest_results = {}
        self.result_lock = threading.Lock()
        self.running = False
        self.thread = None
        
    def capture(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            frame = np.array(screenshot)
            
            if self.use_threading:
                # Start async processing
                self._process_async(frame)
                # Return latest cached results
                with self.result_lock:
                    return self.latest_results.copy()
            else:
                # Process synchronously
                return self.process_frame(frame)
    
    def _process_async(self, frame):
        """Process frame in background thread"""
        if self.thread and self.thread.is_alive():
            return  # Skip if already processing
            
        def process_task():
            results = self.process_frame(frame)
            with self.result_lock:
                self.latest_results = results
        
        self.thread = threading.Thread(target=process_task)
        self.thread.daemon = True
        self.thread.start()
    
    def process_frame(self, frame):
        regions = {
            "Gold": frame[15:70, 365:600],
            "Round": frame[30:70, 1400:1570],
            "Health": frame[10:70, 130:230],
        }

        res = {}
        for k, v in regions.items():
            text = self.OCR_detection(k, v)

            # Post Process
            if k == "Round":
                # Extract numbers like "1/40"
                nums = re.findall(r'\d+', text)
                if len(nums) >= 2:
                    res[k] = {
                        'current': int(nums[0]),
                        'total': int(nums[1])
                    }
                else:
                    res[k] = {'current': None, 'total': None}
            elif k == "Gold":
                # Remove $ and commas from gold amount
                clean = text.replace('$', '').replace(',', '')
                try:
                    res[k] = int(clean) if clean.isdigit() else 0
                except:
                    res[k] = 0
            else:  # Health
                try:
                    res[k] = int(text) if text.isdigit() else 100
                except:
                    res[k] = 100
        
        return res

    def OCR_detection(self, name, frame):
        """Text Detection"""
        try:
            # Preprocess
            mask = self._preprocess(frame)
            
            # OCR with different configs for different text types
            if name == "Round":
                config = '--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789/'
            else:
                config = '--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789$,'
            
            text = pytesseract.image_to_string(mask, config=config)
            
            # Debug: Save image
            debug_path = rf"X:\Dev\BTD6Bot\Assets\Debug\debug_{name}_{int(time.time())}.png"
            cv2.imwrite(debug_path, mask)
            
            clean_text = text.strip()
            print(f"[{time.strftime('%H:%M:%S')}] {name}: {clean_text}")
            return clean_text
            
        except Exception as e:
            print(f"Error processing {name}: {e}")
            return ""

    def _preprocess(self, frame):
        """Preprocess frame for OCR"""
        try:
            # Method 1: Extract white pixels
            white_mask = np.all(frame > 200, axis=2).astype(np.uint8) * 255
            
            # Method 2: Brightness threshold (fallback)
            if cv2.countNonZero(white_mask) < 20:  # Not enough white pixels
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                _, white_mask = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
            
            # Invert for OCR
            result = cv2.bitwise_not(white_mask)
            
            # Upscale if needed
            if result.shape[0] < 50:
                result = cv2.resize(result, None, fx=2, fy=2, 
                                  interpolation=cv2.INTER_CUBIC)
            
            return result
            
        except Exception as e:
            print(f"Preprocessing error: {e}")
            # Return black image as fallback
            return np.zeros((50, 200), dtype=np.uint8)
    
    def save_screenshot(self, frame, filename=None):
        """Save screenshot for debugging"""
        if filename is None:
            filename = f"screenshot_{int(time.time())}.png"
        
        save_path = rf"X:\Dev\BTD6Bot\Assets\Screenshots\{filename}"
        cv2.imwrite(save_path, frame)
        print(f"Saved {save_path}")