#!/usr/bin/env python3
from evdev import InputDevice, list_devices


def get_devices():
    return [InputDevice(fn) for fn in list_devices()]


i = 0
print("Choose the reader from list")
for dev in get_devices():
    print(i, dev.name)
    i += 1