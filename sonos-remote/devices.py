#!/usr/bin/env python3
from reader import Reader, get_devices

i = 0
print("All available devices")
for dev in get_devices():
    print(i, dev.name)
    i += 1

reader = Reader()

print("Waiting for card")
cardid = reader.reader.read_card()
print("Card ID: ", cardid)