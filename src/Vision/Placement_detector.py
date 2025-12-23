# @Author: Simmon
# @Date: 2025-12-18 14:41:12

import pyautogui
import numpy as np
import cv2
from PIL import Image
import time
import math


class Placement_detector:
    def __init__(self, bounds_y1, bounds_x1, bounds_y2, bounds_x2):
        self.radii = [75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325]
        self.max_radius = max(self.radii)
        self.ring_offsets = {
            r: self.build_ring_offsets(r, samples=50) for r in self.radii
        }

        # Store bounds
        self.bounds_y1 = bounds_y1
        self.bounds_x1 = bounds_x1
        self.bounds_y2 = bounds_y2
        self.bounds_x2 = bounds_x2

    def is_valid(self, y, x):
        frame = self.grab_frame(x, y, self.max_radius)

        cx = cy = self.max_radius

        invalid_hits = 0
        total_checks = 0

        for radius in self.radii:
            # Get offsets for this radius
            offsets = self.ring_offsets[radius]

            # Check each sampling point
            for dx, dy in offsets:
                px = cx + dx
                py = cy + dy

                if not (
                    self.bounds_x1 <= px <= self.bounds_x2
                    and self.bounds_y1 <= py <= self.bounds_y2
                ):
                    continue

                r, g, b = frame[py, px]
                # print(f"r {r} | g {g} | b {b} | ({py},{px})")
                total_checks += 1

                if self.is_strong_red(r, g, b):
                    invalid_hits += 1

        if total_checks == 0:
            return True

        ratio = invalid_hits / total_checks
        print(f"Invalid: {ratio:.1%} ({invalid_hits}/{total_checks})")

        return ratio < 0.1

    def is_strong_red(self, r, g, b):
        return r > 180 and r > g * 1.6 and r > b * 1.6

    def build_ring_offsets(self, radius, samples=24):
        offsets = []
        for i in range(samples):
            a = 2 * math.pi * i / samples
            dx = int(round(radius * math.cos(a)))
            dy = int(round(radius * math.sin(a)))
            offsets.append((dx, dy))
        return offsets

    def grab_frame(self, x, y, max_radius):
        size = max_radius * 2 + 2
        region = (x - max_radius, y - max_radius, size, size)
        img = pyautogui.screenshot(region=region)
        return np.array(img)

    # DEBUG
    def save_frame_rgb_txt(self, frame, x, y, filename=None):
        """Save all frame pixels as RGB values in a text file."""
        import os

        # Create directory if needed
        debug_dir = "frame_data"
        os.makedirs(debug_dir, exist_ok=True)

        # Generate filename
        if filename is None:
            from datetime import datetime

            timestamp = datetime.now().strftime("%H%M%S_%f")[:-3]
            filename = f"{debug_dir}/frame_x{x}_y{y}_{timestamp}.txt"

        h, w = frame.shape[:2]

        print(f"Saving {w}x{h} frame to {filename}...")

        with open(filename, "w") as f:
            # Write header
            f.write(f"Frame captured at cursor position: ({x}, {y})\n")
            f.write(f"Frame dimensions: {w} x {h} pixels\n")
            f.write(f"Center pixel (cursor) at: ({w//2}, {h//2})\n")
            f.write("=" * 60 + "\n\n")

            # Write all pixels in grid format
            for y_idx in range(h):
                for x_idx in range(y_idx):
                    r, g, b = frame[y_idx, x_idx]
                    f.write(f"({r:3},{g:3},{b:3}) ")
                f.write("\n")

        print(f"Saved {w*h} pixels to {filename}")
        return filename

    def capture_radius_rings(self, x, y):
        """Capture and save images showing what's at different distances from cursor."""
        # Create visualization image
        vis_size = 200
        visualization = np.ones((vis_size, vis_size, 3), dtype=np.uint8) * 255

        # Draw center point (cursor)
        cv2.circle(visualization, (vis_size // 2, vis_size // 2), 5, (0, 0, 0), -1)

        print("Capturing screenshots at different self.radii...")

        for radius in self.radii:
            # Capture square region
            region_size = radius * 2 + 10
            left = x - region_size // 2
            top = y - region_size // 2

            try:
                # Capture
                screenshot = pyautogui.screenshot(
                    region=(left, top, region_size, region_size)
                )
                img = np.array(screenshot)

                # Save raw screenshot
                filename = f"radius_{radius}px.png"
                Image.fromarray(img).save(filename)
                print(f"Saved: {filename}")

                # Mark the radius distance on visualization
                cv2.circle(
                    visualization,
                    (vis_size // 2, vis_size // 2),
                    int(radius / 2),
                    (200, 200, 200),
                    1,
                )
                cv2.putText(
                    visualization,
                    f"{radius}px",
                    (vis_size // 2 + int(radius / 2) + 5, vis_size // 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    (100, 100, 100),
                    1,
                )

            except Exception as e:
                print(f"Error capturing radius {radius}: {e}")

        # Save visualization
        Image.fromarray(visualization).save("radius_visualization.png")
        print("\nSaved radius_visualization.png")
        print("This shows where each screenshot was taken relative to cursor.")
