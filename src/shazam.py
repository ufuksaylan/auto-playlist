import os
from ShazamAPI import Shazam
import json


def read_file(file_path):
    with open(file_path, "rb") as file:
        content = file.read()
    return content


def recognize_song(file_content, seen_keys):
    shazam = Shazam(file_content)
    data = next(shazam.recognizeSong(), None)

    if data:
        if len(data[1]["matches"]) == 0:
            return None

        track_info = data[1]["track"]
        song = {
            "key": track_info["key"],
            "title": track_info["title"],
            "subtitle": track_info["subtitle"],
        }

        if song["key"] in seen_keys:
            return None

        # print(json.dumps(data, indent=4))
        # print(len(data[1]["matches"]))
        return song

    return None


def find_songs(directory_path="/home/dearmyself/repos/usayla-FPCS.4/src/wavFiles"):
    seen_keys = set()
    track_info = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".wav"):
            file_path = os.path.join(directory_path, filename)
            print(f"Processing {file_path}")
            file_content = read_file(file_path)
            song = recognize_song(file_content, seen_keys)
            if song is not None:
                seen_keys.add(song["key"])
                track_info.append(song)
    return track_info
