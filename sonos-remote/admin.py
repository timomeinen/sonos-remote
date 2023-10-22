#!/usr/bin/env python3

from soco.plugins import sharelink
from reader import Reader

databaseFile = "database.txt"
cardReader = Reader()


def main():
    keep_going = 1

    while keep_going == 1:
        print("Menu of options: ")
        print("1. Add a new playlist or station.")
        option = input("Please enter the number of the action you'd like to take: ")

        if option == "1":
            add_entry()

        keep_going = int(input("Do another (1), or sync and quit (0)? "))
        if keep_going == 0:
            exit(0)


def add_entry():
    print("Please tap NFC tag for this playlist now.")
    tag = cardReader.read_card()
    print("Read tag: ", tag)
    add_spotify_uri(tag)


def add_spotify_uri(tag):
    playlist_url = input("Please paste Spotify Share URL now: ")
    media_uri = sharelink.SpotifyShare().canonical_uri(playlist_url)

    playlist_name = input("What is this playlist called? ")

    playlist = tag + ",spotify," + playlist_name + "," + media_uri + "\n"

    database = open(databaseFile, "a")
    database.write(playlist + "\n")
    database.close()


if __name__ == "__main__":
    main()
