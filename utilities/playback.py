import cv2
import numpy as np
import pyautogui
import threading
import time
import os
import logging
from seleniumbase import BaseCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Playback:
    def __init__(self, driver, fps=10.0):
        self.driver = driver
        self.fps = fps
        self.frames = []
        self.recording = False
        self.lock = threading.Lock()
        self.exception = None
        self.output_filename = None

    def set_output_filename(self, test_method_name):
        """Set the output filename for the recording based on the timestamp and test method name."""
        base_dir = f"recordings"
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
            logger.info(f"Created directories: {base_dir}")

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.output_filename = f"{base_dir}/{timestamp}_{test_method_name}.mp4"
        logger.info(f"Output filename set to: {self.output_filename}")

    def start_recording(self, test_function_name):
        """Start recording the browser window and set the output filename."""
        self.set_output_filename(test_function_name)
        logger.info("Starting recording")
        self.recording = True
        self.record_thread = threading.Thread(target=self._record)
        self.record_thread.start()

    def stop_and_save_recording(self):
        """Stop recording and save the captured video to a file."""
        logger.info("Stopping recording")
        self.recording = False
        if hasattr(self, "record_thread"):
            self.record_thread.join()
        if self.exception:
            logger.error(f"Exception occurred during recording: {self.exception}")
            raise self.exception

        if self.output_filename:
            self._save_video()
        else:
            logger.warning("No output filename specified. Skipping saving video.")

    def _record(self):
        try:
            last_capture_time = time.time()
            while self.recording:
                current_time = time.time()
                if current_time - last_capture_time >= 1.0 / self.fps:
                    screenshot = self._capture_browser_window()
                    if screenshot is not None:
                        with self.lock:
                            self.frames.append(screenshot)
                    last_capture_time = current_time
        except Exception as e:
            logger.exception("Exception occurred in recording thread")
            self.exception = e

    def _capture_browser_window(self):
        try:
            window_rect = self.driver.get_window_rect()
            left, top, width, height = (
                window_rect["x"],
                window_rect["y"],
                window_rect["width"],
                window_rect["height"],
            )

            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        except Exception as e:
            logger.exception("Failed to capture browser window")
            return None

    def _save_video(self):
        logger.info(f"Attempting to save video to {self.output_filename}")
        try:
            with self.lock:
                if not self.frames:
                    logger.warning("No frames captured. Cannot save video.")
                    return

                height, width, _ = self.frames[0].shape
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                out = cv2.VideoWriter(
                    self.output_filename, fourcc, self.fps, (width, height)
                )

                if not out.isOpened():
                    logger.error("Failed to open video file for writing.")
                    return

                for frame in self.frames:
                    out.write(frame)

                out.release()
                logger.info(f"Video saved successfully as {self.output_filename}")
        except Exception as e:
            logger.exception(f"Exception occurred while saving video: {str(e)}")
