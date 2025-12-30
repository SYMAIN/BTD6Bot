import pyautogui
import numpy as np
import cv2
from config.settings import settings
from config.constants import (
    MONKEY_EXIST_MENU_COLOR,
    PLACEMENT_DETECTION_RADII,
    RADIUS_SAMPLE_SIZE,
    RADIUS_SAMPLE_EXPONENT,
    RADIUS_WEIGHT_EXPONENT,
    MAX_SAMPLE_MULTIPLIER,
    SMALL_RADIUS_ACCEPT_COUNT,
    SMALL_RADIUS_ACCEPT_THRESHOLD,
    VALID_SCORE,
)
from utils.logger import logger
import numpy as np
import time
from PIL import Image


class PlacementDetector:
    def __init__(self):
        # Ensure radii are processed from smallest to largest
        self.radii = sorted(PLACEMENT_DETECTION_RADII)
        self.max_radius = max(self.radii)
        self.sample_exponent = RADIUS_SAMPLE_EXPONENT
        # Build per-radius offsets using exponential sampling:
        # smaller radii get more samples for better accuracy
        self.ring_offsets = {
            r: self.build_ring_offsets(r, samples=self._samples_for_radius(r))
            for r in self.radii
        }
        # Weight rings so smaller radii influence the final score more
        # Use a separate exponent so weighting can be tuned independently
        self.ring_weights = {
            r: (self.max_radius / r) ** RADIUS_WEIGHT_EXPONENT for r in self.radii
        }

        # Game bounds
        game_size = settings.GAME_SIZE
        self.bounds_y1, self.bounds_x1, self.bounds_y2, self.bounds_x2 = game_size

    def is_valid(self, y: int, x: int) -> bool:
        """Simpler: Check actual screen pixels without frame capture.

        Computes per-radius invalid fractions, weights smaller radii more, and
        allows an early exit if a ring is strongly invalid. Also accepts early
        if the smallest N rings look clean (helps small-range towers).
        """
        frame = self.grab_frame(x, y, self.max_radius)

        weighted_invalid = 0.0
        weight_sum = 0.0

        # Per-radius immediate fail threshold: if a ring shows very high
        # invalid fraction, consider the placement invalid immediately.
        per_radius_fail_threshold = max(0.5, VALID_SCORE * 2)

        # Small-radius early-accept tracking
        small_invalid = 0
        small_total = 0
        small_count = SMALL_RADIUS_ACCEPT_COUNT

        for i, radius in enumerate(self.radii):
            offsets = self.ring_offsets[radius]
            ring_invalid = 0
            ring_total = 0

            for dx, dy in offsets:
                screen_x = x + dx
                screen_y = y + dy

                if not (
                    self.bounds_x1 <= screen_x <= self.bounds_x2
                    and self.bounds_y1 <= screen_y <= self.bounds_y2
                ):
                    continue

                # Convert absolute screen coordinates to local frame coordinates.
                local_x = screen_x - (x - self.max_radius)
                local_y = screen_y - (y - self.max_radius)

                if not (
                    0 <= local_x < frame.shape[1] and 0 <= local_y < frame.shape[0]
                ):
                    continue

                r, g, b = frame[local_y, local_x]
                ring_total += 1
                ring_invalid += self.is_strong_black(r, g, b)

            if ring_total == 0:
                continue

            ring_frac = ring_invalid / ring_total

            # Immediate fail for strongly invalid rings (helps small-radius cases)
            if ring_frac >= per_radius_fail_threshold:
                logger.debug(
                    f"Immediate fail at radius {radius}: {ring_invalid}/{ring_total} ({ring_frac:.2%})"
                )
                return False

            # Accumulate for an early-accept based on smallest N rings
            if i < small_count:
                small_invalid += ring_invalid
                small_total += ring_total
                # Once we've processed the last small ring, check accept condition
                if i == small_count - 1 and small_total > 0:
                    small_frac = small_invalid / small_total
                    if small_frac <= SMALL_RADIUS_ACCEPT_THRESHOLD:
                        logger.debug(
                            f"Early accept based on smallest {small_count} rings: {small_invalid}/{small_total} ({small_frac:.2%})"
                        )
                        return True

            weight = self.ring_weights.get(radius, 1.0)
            weighted_invalid += ring_frac * weight
            weight_sum += weight

            logger.debug(
                f"Radius: {radius} | invalid: {ring_frac:.4f} | sample_size: {len(offsets)}"
            )

        if weight_sum == 0:
            return True

        final_score = weighted_invalid / weight_sum
        logger.info(f"Validation Score (weighted): {final_score:.2%}")
        return final_score < VALID_SCORE

    def is_strong_black(self, r: int, g: int, b: int) -> int:
        """Using Black/White placement circle. Checking for high black pixels"""
        color_tolerance = 10
        # Treat near-black as invalid
        if r < color_tolerance and g < color_tolerance and b < color_tolerance:
            return 1
        # Treat white and other colors as non-invalid
        return 0

    def is_strong_red(self, r, g, b):
        """Using Red/Grey transparency. CHecking for high red pixels"""
        return r > 180 and r > g * 1.6 and r > b * 1.6

    def build_ring_offsets(self, radius: int, samples: int = 24) -> list:
        """Create circle sampling points."""
        import math

        offsets = []
        for i in range(samples):
            angle = 2 * math.pi * i / samples
            dx = int(round(radius * math.cos(angle)))
            dy = int(round(radius * math.sin(angle)))
            offsets.append((dx, dy))
        return offsets

    def _samples_for_radius(self, radius: int) -> int:
        """Compute number of samples for a radius: smaller radii get more samples.

        Uses exponential scaling so smaller radii are sampled more densely.
        """
        min_samples = 8
        # Allow a larger multiplier to let tiny radii sample more densely when needed
        max_samples = max(8, RADIUS_SAMPLE_SIZE * MAX_SAMPLE_MULTIPLIER)
        samples = int(
            round(
                RADIUS_SAMPLE_SIZE * (self.max_radius / radius) ** self.sample_exponent
            )
        )
        return max(min_samples, min(samples, max_samples))

    def grab_frame(self, x: int, y: int, radius: int):
        """Capture square region around point."""
        size = radius * 2 + 2
        region = (x - radius, y - radius, size, size)
        img = pyautogui.screenshot(region=region)
        return np.array(img)

    def _count_target_pixels(
        self, img, target_rgb: np.ndarray, tolerance: int = 0
    ) -> int:
        """Count pixels that match the target RGB.

        If `tolerance` is 0 or None, performs an exact match. Accepts either a
        PIL Image or a numpy array. Returns the number of matching pixels (int).
        On error, logs a warning and returns 0.
        """
        try:
            # If PIL Image, convert to RGB numpy array
            if hasattr(img, "mode"):
                img = img.convert("RGB")
                arr = np.array(img)
            else:
                arr = img

            # If image has alpha channel, drop it
            if arr.ndim == 3 and arr.shape[2] == 4:
                arr = arr[:, :, :3]

            # Convert to signed ints to avoid uint8 wrap-around on subtraction
            arr = arr.astype(np.int16)
            target = np.array(target_rgb[:3]).astype(np.int16)

            if tolerance is None:
                tolerance = 0

            color_diff = np.abs(arr - target)

            if tolerance == 0:
                matches = np.all(color_diff == 0, axis=2)
            else:
                matches = np.all(color_diff <= tolerance, axis=2)

            return int(np.count_nonzero(matches))
        except Exception as e:
            logger.warning(f"_count_target_pixels error: {e}")
            return 0

    def verify_monkey_selected(self, y: int, x: int) -> bool:
        """Faster verification using numpy array operations."""

        TARGET_RGB = np.array(MONKEY_EXIST_MENU_COLOR, dtype=np.int16)

        # Click monkey
        pyautogui.moveTo(x, y)
        pyautogui.click()
        time.sleep(1)  # Wait for screen to appear

        # Capture full screen then count matches
        screenshot = pyautogui.screenshot()
        pyautogui.press("esc")  # Cancel Menu

        match_count = self._count_target_pixels(screenshot, TARGET_RGB)

        logger.debug(f"Upgrade UI pixels: {match_count}")
        return match_count > 1000

    def capture_radius_rings(self, x, y):
        """Capture and save images showing what's at different distances from cursor."""
        # Create visualization image
        vis_size = 200
        visualization = np.ones((vis_size, vis_size, 3), dtype=np.uint8) * 255

        # Draw center point (cursor)
        cv2.circle(visualization, (vis_size // 2, vis_size // 2), 5, (0, 0, 0), -1)

        logger.info("Capturing screenshots at different self.radii...")

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
                logger.info(f"Saved: {filename}")

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
                logger.error(f"Error capturing radius {radius}: {e}")

        # Save visualization
        Image.fromarray(visualization).save("radius_visualization.png")
        logger.info("\nSaved radius_visualization.png")
