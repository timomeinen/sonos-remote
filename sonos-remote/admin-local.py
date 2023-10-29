#!/usr/bin/env python3

import soco
from soco.plugins import sharelink

MUSIC_SERVICE = "spotify"
DATABASE_FILENAME = "database.txt"

speakers = list(soco.discover())


def main():
    while True:
        add_entry()
        print()
        quit_program_prompt()


def add_entry():
    tag = read_nfc_tag()
    speaker = read_speaker()
    media_uri = read_media_uri()
    playlist = read_playlist(media_uri, tag, speaker)

    create_database_entry(playlist)


def read_nfc_tag():
    tag = input("Please type NFC tag for this playlist now: ")
    return tag


def read_speaker():
    for i, speaker in enumerate(speakers, start=1):
        print(i, speaker.player_name)
    speaker_index = int(input("Select speaker: "))
    return speakers[speaker_index - 1].player_name


def read_media_uri():
    playlist_url = input("Please paste Spotify Share URL now: ")
    media_uri = sharelink.SpotifyShare().canonical_uri(playlist_url)
    return media_uri


def read_playlist(media_uri, tag, speaker):
    playlist_name = input("What is this playlist called? ")
    playlist = ','.join([tag, speaker, MUSIC_SERVICE, playlist_name, media_uri])
    return playlist


def create_database_entry(playlist):
    print("DB Entry: ", playlist)
    with open(DATABASE_FILENAME, "a") as database:
        database.write(playlist + "\n")


def quit_program_prompt():
    quit_program = input("Quit? (y/N) ")
    if quit_program == "y":
        exit(0)


if __name__ == "__main__":
    main()
