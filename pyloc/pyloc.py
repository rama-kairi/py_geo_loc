import time
from typing import Callable, Dict

import requests


class Retry(object):
    """class providing a decorator for retrying HTTP requests"""

    def __init__(self, nbtimes: int, wait_time_sec: int = 0):
        self.nbtimes = nbtimes
        self.times = 0
        self.errors = []
        self.wait_time_sec = wait_time_sec

    def __call__(self, func: Callable):
        def wrapper(*args, **kwargs):
            self.times += 1
            if self.nbtimes != self.times:
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    print(f"error: retrying after waiting for {self.wait_time_sec} sec")
                    if hasattr(err, "message"):
                        self.errors.append(err.message)
                    else:
                        self.errors.append(err)
                    time.sleep(self.wait_time_sec)
                    wrapper(*args, **kwargs)
            else:
                print(
                    f"fails to execute retried {self.times} times. Lists of errors : {self.errors}"
                )

        return wrapper


@Retry(nbtimes=5, wait_time_sec=5)
def make_requests(loc: str) -> Dict:
    url = f"https://nominatim.openstreetmap.org/search?q={loc}&format=json&limit=1"
    resp = requests.get(url, timeout=0.5)
    if resp.status_code != 200:
        raise ValueError("Error with request")
    return resp.json()[0]


def get_lat_long(loc: str) -> Dict:
    res = make_requests(loc)
    return {"lat": res["lat"], "lon": res["lon"]} if res else {}
