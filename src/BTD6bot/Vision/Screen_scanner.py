# @Author: Simmon
# @Date: 2025-11-21 11:43:50

import mss
import time
import threading
import numpy as np
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'X:\Tesseract\tesseract.exe'

class Screen_scanner:
    def __init__(self):
        self.running = False
        self.capture_thread = None
        self.process_thread = None
    
    def start(self):
        self.running = True
        print("Screen_scanner starting...")
        self.process_thread = threading.Thread(target=self._process_loop, daemon=True)
        self.process_thread.start()
    
    def stop(self):
        self.running = False
        if self.process_thread:
            self.process_thread.join(timeout=1)
        print("Screen_scanner stopped")
    
    def _process_loop(self):
        """Combined capture and processing in one thread"""
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            
            while self.running:
                start_time = time.time()
                
                # 1. Capture screen
                screenshot = sct.grab(monitor)
                frame = np.array(screenshot)
                
                # 2. Process immediately
                self._process_frame(frame)
                
                # 3. Maintain approximately 1 FPS (or adjust as needed)
                elapsed = time.time() - start_time
                sleep_time = max(0, 1.0 - elapsed)
                time.sleep(sleep_time)
    
    def _process_frame(self, frame):
        """Process a single frame"""
        try:
            # Gold detection
            gold_region = frame[15:70, 365:600]
            # Preprocess
            mask = self._preprocess(gold_region)
            # OCR
            text = pytesseract.image_to_string(
                mask, 
                config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789$,'
            )
            cv2.imwrite(f"debug_Gold.png", mask)
            print(f"Gold: {text.strip()}")
            
        except Exception as e:
            print(f"Error processing frame: {e}")
    
    def _preprocess(self, frame):
        # Create a mask where pixels are mostly white (all channels > 200)
        white_mask = np.all(frame > 200, axis=2).astype(np.uint8) * 255
        
        #Alternative - look for bright pixels (if method 1 fails)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, bright_mask = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
        
        combined = cv2.bitwise_or(white_mask, bright_mask)
        if frame.shape[0] < 50:  # If ROI height is less than 50px
            result = cv2.resize(result, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            
        # Invert for OCR
        result = cv2.bitwise_not(combined)
        return result
    
    
    def save_screenshot(self, frame, filename="screenshot.png"):
        cv2.imwrite(rf"X:\Dev\BTD6Bot\Assets\Screenshots\{filename}", frame)
        print(f"Saved {filename}")