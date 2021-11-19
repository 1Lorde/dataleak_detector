from concurrent.futures import ThreadPoolExecutor

from api import update_allowed_drives
from usb import watch_drives_win, watch_drives_linux
from utils import get_os

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as executor:
        future = executor.submit(update_allowed_drives)
        print("Task [Auto updating] started")

        if get_os() == 'Windows':
            future = executor.submit(watch_drives_win)
        else:
            future = executor.submit(watch_drives_linux)
        print("Task [USB-device watch] started")