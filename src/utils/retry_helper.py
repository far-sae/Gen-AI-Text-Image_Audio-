
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging

logger = logging.getLogger(__name__)

def retry_on_exception(func=None, *, attempts=3):
    def _decorator(f):
        @retry(stop=stop_after_attempt(attempts), wait=wait_exponential(multiplier=1, min=1, max=10),
               retry=retry_if_exception_type(Exception))
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapped
    if func:
        return _decorator(func)
    return _decorator
