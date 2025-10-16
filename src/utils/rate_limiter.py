import time
from threading import Lock

class SimpleRateLimiter:
    def __init__(self, calls_per_sec: float):
        self.interval = 1.0 / calls_per_sec
        self.lock = Lock()
        self._last = 0.0

    def wait(self):
        with self.lock:
            now = time.time()
            diff = self.interval - (now - self._last)
            if diff > 0:
                time.sleep(diff)
            self._last = time.time()
