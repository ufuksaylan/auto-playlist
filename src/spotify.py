from dotenv import find_dotenv, load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


load_dotenv(find_dotenv())
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")


def get_auth_code():
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET
    redirect_uri = REDIRECT_URI  # This needs to match the redirect URI you set up in your Spotify app
    scope = "playlist-modify-public"

    # Spotipy will prompt the user to login if necessary and return the access token
    token = spotipy.util.prompt_for_user_token(
        username="",
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )

    return token


def search_spotify(track_name, artist_name):
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Create a query string with the track name and artist name
    query = f"track:{track_name} artist:{artist_name}"

    # Search Spotify for the track
    results = sp.search(q=query, type="track")

    # Return the first result, if any
    if results["tracks"]["items"]:
        return results["tracks"]["items"][0]["id"]  # Return the Spotify ID of the track
    else:
        return None


def get_current_username(access_token):
    # Create a Spotify object with the access token
    sp = spotipy.Spotify(auth=access_token)

    # Get the current user
    current_user = sp.current_user()

    # Return the username
    return current_user["id"]


def create_playlist_and_add_tracks(
    spotify_username, access_token, playlist_name, track_ids
):
    # Create a SpotifyOAuth object
    scope = "playlist-modify-public"  # Use "playlist-modify-private" if you want the playlist to be private
    sp = spotipy.Spotify(auth=access_token)

    # Create a new playlist
    playlist = sp.user_playlist_create(spotify_username, playlist_name, public=True)

    # Get the playlist's ID
    playlist_id = playlist["id"]

    # Add the tracks to the playlist
    sp.playlist_add_items(playlist_id, track_ids)
