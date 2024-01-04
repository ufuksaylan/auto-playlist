from yamnet.inference import process_directory, create_directory, delete_directory
from audio_converter import extract_segments, get_number_of_segments
from shazam import find_songs
import sys
from spotify import (
    search_spotify,
    get_auth_code,
    get_current_username,
    create_playlist_and_add_tracks,
)
import os


def check_file_exists(file_path):
    if not os.path.exists(file_path):
        sys.exit(f"The file '{file_path}' does not exist.")


def print_found_songs(data):
    for i, item in enumerate(data, start=1):
        print(f"{i}. Title: {item['title']}\n   Subtitle: {item['subtitle']}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a file path as an argument.")
        sys.exit(1)

    file_path = sys.argv[1]
    check_file_exists(file_path)

    playlist_name = input("Enter the album name: ")
    create_directory()

    number_of_segments = get_number_of_segments(file_path)
    extract_segments(file_path)
    process_directory(number_of_segments)
    tracks = find_songs()
    delete_directory()

    print("Following songs are found in the video:")
    print_found_songs(tracks)

    spotify_track_ids = []

    for track in tracks:
        song = search_spotify(track["title"], track["subtitle"])
        song_uri_format = f"spotify:track:{song}"
        if song:
            spotify_track_ids.append(song_uri_format)

    if len(spotify_track_ids) == 0:
        print("no songs is found on spotify")
        sys.exit()

    auth_code = get_auth_code()

    spotify_username = get_current_username(auth_code)

    create_playlist_and_add_tracks(
        spotify_username, auth_code, playlist_name, spotify_track_ids
    )
