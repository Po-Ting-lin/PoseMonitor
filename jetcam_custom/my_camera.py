import atexit
import cv2
import threading
import time
from core.rate_counter import RateCounter


class MyCamera(object):
    def __init__(self, device, width, height, fps):
        self.width = width
        self.height = height
        self.is_capturing = False
        self.capture_thread = None
        self.capture_counter = RateCounter("capture rate", 50)
        self.process_callback = None
        try:
            self.cap = cv2.VideoCapture(device)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FPS, fps)
            re, image = self.cap.read()
            if not re:
                raise RuntimeError('Could not read image from camera.')
        except Exception:
            raise RuntimeError(
                'Could not initialize camera.  Please see error trace.')
        atexit.register(self.cap.release)

    def start_capture(self, process_callback):
        if not self.is_capturing:
            print("start capture")
            self.is_capturing = True
            self.process_callback = process_callback
            self.capture_counter.start()
            self.capture_thread = threading.Thread(target=self._read, name="capture thread")
            self.capture_thread.daemon = True  # kill the thread when sys.exit
            self.capture_thread.start()

    def stop_capture(self):
        if self.is_capturing:
            self.is_capturing = False
            self.capture_thread.join()
            print("stop capture")

    def _read(self):
        while self.is_capturing:
            re, image = self.cap.read()
            if re:
                self.process_callback(cv2.resize(image, (int(self.width), int(self.height))))
            else:
                raise RuntimeError('Could not read image from camera')
            self.capture_counter.add_to_count()
            time.sleep(0.04)
