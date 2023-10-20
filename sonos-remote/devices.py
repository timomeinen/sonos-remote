#!/usr/bin/env python3
import time

from reader import Reader, get_devices

i = 0
print("All available devices")
for dev in get_devices():
    print(i, dev.name)
    i += 1

reader = Reader()

while True:
    # slow down the card reading while loop
    time.sleep(0.2)

    print("Waiting for card")
    cardid = reader.reader.read_card()
    print("Card ID: ", cardid)
