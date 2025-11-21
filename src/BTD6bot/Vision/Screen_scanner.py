# @Author: Simmon
# @Date: 2025-11-21 11:43:50
# @Last Modified by:   undefined
# @Last Modified time: 2025-11-21 11:43:50

import mss
import time
import threading
from queue import Queue
import numpy as np
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
  
    def start_processing(self):
        screenshotter = Screenshot()
        screenshotter.start() 

        while True:
            frame = screenshotter.get_latest_frame()
            if frame is not None:
                self.process_frame(frame)  # Takes however long it needs
            else:
                time.sleep(0.01)  # Small sleep if no new frame
    def process_frame(self, frame):
        """
        Dissect the frame to find information
        - Blood Path
        - Gold
        - Health
        - Round
        """
        pass
    def detect_round(self):
        pass
    def detect_gold(self):
        pass
    def detect_health(self):
        pass
    def detect_path(self):
        pass

  

class Screenshot:
    def __init__(self):
        self.sct = mss.mss()
        self.latest_frame = None
        self.frame_ready = threading.Event()
        self.running = False
    
    def capture_thread(self):
        """Always capture at exactly 1 FPS"""
        while self.running:
            start = time.time()
            
            # Capture
            screenshot = self.sct.grab(self.sct.monitors[1])
            self.latest_frame = np.array(screenshot)
            self.frame_ready.set()  # Signal that new frame is available
            
            # Maintain exact 1 FPS
            elapsed = time.time() - start
            time.sleep(max(0, 1.0 - elapsed))
    
    def get_latest_frame(self):
        """Main thread gets latest frame (drops old ones)"""
        if self.frame_ready.is_set():
            self.frame_ready.clear()
            return self.latest_frame.copy()
        return None
    
    def start(self):
        self.running = True
        threading.Thread(target=self.capture_thread, daemon=True).start()
    

    def stop(self):
        self.running = False
        self.thread.join()  
        self.sct.close()