import os
import platform
import socket

from getmac import get_mac_address


def get_mac():
    return get_mac_address().upper()


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def get_user():
    return os.getlogin()


def get_os():
    return platform.system()


def block_linux(user):
    # os.system('usermod -L ' + user)
    os.system('pkill -KILL -u ' + user)

def block_win(user):
    # os.system('usermod -L ' + user)
    os.system('locker/Block.exe')
