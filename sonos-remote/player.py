#!/usr/bin/env python3
import time

from soco.discovery import by_name
from soco.plugins import sharelink

from reader import Reader

speaker = by_name("Move")
reader = Reader()

databaseFile = "database.txt"  # name of the local database text file
defaultVolume = 20

playlists = []


def main():
    load_playlists()

    while True:
        # slow down the card reading while loop
        time.sleep(0.2)

        print("Waiting for card")
        tag = reader.reader.read_card()
        print("Card TAG: ", tag)
        play_nfc_stream(tag)


def play_nfc_stream(nfc_uid):
    x = 0
    for i in playlists:
        tag = str(i[0]).lower()

        if tag == nfc_uid:
            print("Found card in database", tag)
            service = identify_service(playlists[x])

            if service == "spotify":
                play_spotify_playlist(playlists[x])
            elif service == "utility":
                utility_controls(playlists[x])
            else:
                print("Error: Unknown Service")

            break

        x = x + 1


def load_playlists():
    global databaseFile
    global playlists

    playlists = []

    print("Load Database")
    with open(databaseFile, "r") as fp:
        for playlist in fp:
            playlists.append(playlist.strip().split(","))

    print(playlists)
    return playlists


def identify_service(playlist_entry):
    return playlist_entry[1]


def play_spotify_playlist(playlists):
    playlist_name = playlists[2]
    playlist_url = playlists[3]

    media_uri = sharelink.SpotifyShare().canonical_uri(playlist_url)
    print("Media URI", media_uri)

    speaker.clear_queue()
    sharelink.ShareLinkPlugin(speaker).add_share_link_to_queue(media_uri, position=1, as_next=True)
    speaker.play_from_queue(0, start=True)
    # speaker.play_uri(media_uri)

    print("Playing the Spotify playlist: ", playlist_name)


def utility_controls(playlists):
    global defaultVolume
    global speaker
    control = playlists[2].strip()

    if control == "vol reset":
        speaker.volume = defaultVolume
    elif control == "vol down":
        speaker.volume = (defaultVolume - 10)


if __name__ == "__main__":
    main()
