#!/usr/bin/env python3
import time

from reader import Reader
from soco.discovery import by_name

speaker = by_name("Move")

# i = 0
# print("All available devices")
# for dev in get_devices():
#     print(i, dev.name)
#     i += 1

reader = Reader()

while True:
    # slow down the card reading while loop
    time.sleep(0.2)

    print("Waiting for card")
    cardid = reader.reader.read_card()
    print("Card ID: ", cardid)

    if cardid == "0012071435":
        print("Play chillout")
        speaker.play_uri('https://wdr-1live-chillout.icecast.wdr.de/wdr/1live/chillout/mp3/128/stream.mp3')
    elif cardid == "0012253663":
        print("Play Dancehits")
        speaker.play_uri('https://wdr-1live-dancehits.icecast.wdr.de/wdr/1live/dancehits/mp3/128/stream.mp3')
    elif cardid == "0012298943":
        print("STOP")
        speaker.stop()


