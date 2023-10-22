from soco.discovery import by_name

wohnzimmer = by_name("Wohnzimmer")
wohnzimmer.volume = 20
wohnzimmer.play_uri('https://wdr-1live-chillout.icecast.wdr.de/wdr/1live/chillout/mp3/128/stream.mp3')