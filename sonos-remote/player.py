#!/usr/bin/env python3
import time

import soco
from soco import SoCo
from soco.plugins import sharelink

from reader import Reader

DATABASE_FILENAME = "database.txt"
DEFAULT_VOLUME = 20


def main():
    playlists = load_playlists()
    speakers = list(soco.discover())
    reader = Reader()

    while True:
        # slow down the card reading while loop
        time.sleep(0.2)

        print("Waiting for card")
        read_card_tag = reader.reader.read_card()
        print("Card TAG: ", read_card_tag)
        play_nfc_stream(read_card_tag, playlists, speakers)


def play_nfc_stream(requested_tag, playlists, speakers):
    for playlist in playlists:
        # Example: 1,Bjarne,spotify,name,spotify:track:793rGBvVCGn2FFiNBALwgM
        tag = str(playlist[0]).lower()

        if tag == requested_tag:
            print("Found card in database", tag)
            speaker_name = playlist[1]
            service = playlist[2]

            if service == "spotify":
                speaker: SoCo = get_speaker(speakers, speaker_name)
                play_spotify_playlist(playlist, speaker)
            elif service == "utility":
                utility_controls(playlist)
            else:
                print("Error: Unknown Service")

            break


def get_speaker(speakers, speaker_name: str):
    for s in speakers:
        if s.player_name == speaker_name:
            return s
    raise "Could not find speaker with name: " + speaker_name


def load_playlists():
    print("Load Database:")
    playlists = []
    with open(DATABASE_FILENAME, "r") as database:
        for playlist in database:
            playlist_entry = playlist.strip().split(",")
            print("Entry:", playlist_entry)
            playlists.append(playlist_entry)
    return playlists


def play_spotify_playlist(playlist, speaker):
    playlist_name = playlist[3]
    playlist_url = playlist[4]

    media_uri = sharelink.SpotifyShare().canonical_uri(playlist_url)
    print("Media URI", media_uri)

    speaker.clear_queue()
    sharelink.ShareLinkPlugin(speaker).add_share_link_to_queue(media_uri, position=1, as_next=True)
    speaker.play_from_queue(0, start=True)

    print("Playing on", speaker.player_name, speaker.ip_address, "Spotify:", playlist_name)


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
