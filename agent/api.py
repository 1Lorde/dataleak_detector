import os
import time
from hashlib import sha256

import requests

from config import management_host, management_port, local_db_filename, update_timeout

check_url = "http://{}:{}/devices/check".format(management_host, management_port)
allowed_url = "http://{}:{}/devices/allowed".format(management_host, management_port)
allowed_hash_url = "http://{}:{}/devices/allowed/hash".format(management_host, management_port)


def is_allowed_latest():
    try:
        if not os.path.exists(local_db_filename):
            return False

        response = requests.get(allowed_hash_url).text
        with open(local_db_filename, 'r') as f:
            hashes = f.read()

        h = sha256()
        h.update(hashes.encode('utf-8'))

        if response == h.hexdigest():
            print('[Auto updating task] Local database of allowed devices are latest')
            return True
        else:
            print('[Auto updating task] Local database of allowed devices are outdated')
            return False

    except Exception as e:
        print('[Auto updating task] Can`t get hash of allowed devices database, cause ' + str(type(e).__name__))


def update_allowed_drives():
    while True:
        if not is_allowed_latest():
            try:
                response = requests.get(allowed_url).text
                with open(local_db_filename, 'w') as f:
                    f.writelines(response)
                    print('[Auto updating task] List of allowed devices successfully updated')
            except Exception as e:
                print('[Auto updating task] List of allowed devices not updated, cause ' + str(type(e).__name__))

        time.sleep(update_timeout)


def offline_check(serial):
    if not os.path.exists(local_db_filename):
        print('Local database is empty. Drive {} are blocked'.format(serial))
        return False

    h = sha256()
    h.update(serial.encode('utf-8'))
    with open(local_db_filename, 'r') as f:
        hashes = f.readline().split(';')
        if not h.hexdigest() in hashes:
            print('Drive {} not allowed'.format(serial))
            return False
        else:
            return True
