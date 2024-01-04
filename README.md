# AutoPlaylist: A Shazam-Inspired Spotify Playlist Creator

## Introduction

AutoPlaylist is a tool designed to create Spotify playlists based on the soundtracks and background music of videos or movies. This project harnesses the capabilities of TensorFlow's YAMNet model, a deep net trained for audio event classification, and utilizes a Shazam-like song recognition functionality to identify songs. After identifying the music, the project interfaces with the Spotify API to automatically create a Spotify playlist comprising these songs.

## Technologies Used

- **TensorFlow 2.x**: For implementing the YAMNet model for audio event classification.
- **YAMNet Model**: A deep net trained for audio event classification.
- **FFmpeg**: For processing video and audio files.
- **Spotify API**: To create playlists and interact with Spotify's music library.
- **Python**: The main programming language used for the project.

## Prerequisites

This project requires the following software:

- TensorFlow 2.x
- YAMNet Model
- FFmpeg
- Spotify developer account to access the Spotify API: CLIENT_ID, CLIENT_SECRET, and REDIRECT_URI should be specified in the env file.

For TensorFlow installation, follow the instructions provided in the [TensorFlow Model Garden Repository.](https://github.com/tensorflow/models)

## Installation

- First, install the required Python libraries. You can do this by running:

```shell
pip install -r requirements.txt
```

Please note that this script also requires FFmpeg to be installed on your system. Refer to the instructions in the previous messages on how to install FFmpeg on different operating systems.

- Setup Spotify Application:

To use this script, you need to have a Spotify account and you need to create a Spotify application to get the required credentials (client ID, client secret, redirect URI). Set these credentials as environment variables. This can typically be done in a .env file in the root directory of your project. Your .env file should look like this:

```shell
CLIENT_ID=<Your Spotify Client ID>
CLIENT_SECRET=<Your Spotify Client Secret>
REDIRECT_URI=<Your Spotify App Redirect URI>
```

Please replace <Your Spotify Client ID>, <Your Spotify Client Secret> and <Your Spotify App Redirect URI> with your actual credentials.

## Usage

Ensure that you are in the src directory of the project. This is important because the script uses relative imports which will not work if the script is run from a different location.

You can run the script from the command line with the video file as an argument. Here is the syntax:

```shell
python main.py <file_path>
```

Where <file_path> is the path to your video file. For example:

```shell
python main.py ../videos/video.mp4
```
