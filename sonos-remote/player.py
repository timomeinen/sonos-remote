#!/usr/bin/env python3
import time

from soco.plugins import sharelink

from reader import Reader

DATABASE_FILENAME = "database.txt"
DEFAULT_VOLUME = 20


def main():
    playlists = load_playlists()
    reader = Reader()

    while True:
        # slow down the card reading while loop
        time.sleep(0.2)

        print("Waiting for card")
        read_card_tag = reader.reader.read_card()
        print("Card TAG: ", read_card_tag)
        play_nfc_stream(read_card_tag, playlists)


def play_nfc_stream(requested_tag, playlists):
    for playlist in playlists:
        # Example: 1,Bjarne,spotify,name,spotify:track:793rGBvVCGn2FFiNBALwgM
        tag = str(playlist[0]).lower()

        if tag == requested_tag:
            print("Found card in database", tag)
            service = playlist[2]

            if service == "spotify":
                play_spotify_playlist(playlist)
            elif service == "utility":
                utility_controls(playlist)
            else:
                print("Error: Unknown Service")

            break


def load_playlists():
    print("Load Database:")
    playlists = []
    with open(DATABASE_FILENAME, "r") as database:
        for playlist in database:
            playlist_entry = playlist.strip().split(",")
            print("Entry:", playlist_entry)
            playlists.append(playlist_entry)
    return playlists


def play_spotify_playlist(playlist):
    speaker = playlist[2]
    playlist_name = playlist[3]
    playlist_url = playlist[4]

    media_uri = sharelink.SpotifyShare().canonical_uri(playlist_url)
    print("Media URI", media_uri)

    speaker.clear_queue()
    sharelink.ShareLinkPlugin(speaker).add_share_link_to_queue(media_uri, position=1, as_next=True)
    speaker.play_from_queue(0, start=True)

    print("Playing Spotify:", playlist_name)


def utility_controls(playlist):
    global DEFAULT_VOLUME
    speaker = playlist[2]
    control = playlist[3].strip()

    if control == "vol reset":
        speaker.volume = DEFAULT_VOLUME
    elif control == "vol down":
        speaker.volume = speaker.volume - 5
    elif control == "vol up":
        speaker.volume = speaker.volume + 5

    print("New volume:", speaker.volume)


if __name__ == "__main__":
    main()
