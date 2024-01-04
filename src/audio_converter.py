import subprocess
import math
import multiprocessing


def extract_audio(segment, input_file, segment_duration):
    start_time = segment * segment_duration
    audio_file = f"wavFiles/segment{segment}.wav"
    command = f"ffmpeg -i {input_file} -ss {start_time} -t {segment_duration} -vn {audio_file}"
    subprocess.call(command, shell=True)


def get_duration(input_file):
    return float(
        subprocess.check_output(
            f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {input_file}",
            shell=True,
        )
    )


def get_number_of_segments(input_file, segment_duration=8):
    duration = get_duration(input_file)
    segments = math.ceil(
        duration / segment_duration
    )  # calculate total number of segments based on segment_duration
    return segments


def extract_segments(input_file, segment_duration=8):
    duration = get_duration(input_file)
    segments = math.ceil(
        duration / segment_duration
    )  # calculate total number of segments based on segment_duration
    with multiprocessing.Pool() as pool:
        pool.starmap(
            extract_audio, [(i, input_file, segment_duration) for i in range(segments)]
        )
