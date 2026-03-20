# - Spotify Purger - 
# tracks and deletes skipped songs of off a particular playlist.

# By Jesse Mogg, 11/08/2024

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import json
from requests.exceptions import ReadTimeout


# -- Setup --
# Spotify API credentials
SPOTIPY_CLIENT_ID = ""
SPOTIPY_CLIENT_SECRET = "_"
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"

# Playlist ID
PLAYLIST_ID = ""

# Set up spotipy object
scope = "user-library-read playlist-modify-public playlist-modify-private user-read-playback-state"
auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager, requests_timeout=3, retries=10)


# -- App Functionality --
# Handles 401 error of expired token
def get_current_playback():
    try:
        return sp.current_playback()
    
    except (ReadTimeout, ConnectionError):
        print("Requests error, retrying...")
        return get_current_playback()

    except spotipy.exceptions.SpotifyException as e:
        if e.http_status == 401:  # Token expired, refresh it
            sp.auth_manager.get_access_token(as_dict=False)
            return get_current_playback()
        
        else:
            raise e

print("Running... prolly..")

last_playback = None
while True:
    # Check every 3 seconds
    time.sleep(3)

    # Retrieve current playback
    current_playback = get_current_playback()

    # If there is no playback, reset playback to avoid unjust killing
    # Also avoids running redundant code
    if not current_playback:
        last_playback = None

        continue

    # If not playing, skip
    if not current_playback["is_playing"]:
        continue

    # If playback is not of the correct playlist, or some error occurs (no context or uri), skip
    try:
        if not current_playback["context"]["uri"] == f"spotify:playlist:{PLAYLIST_ID}":
            continue
    except:
        continue

    # Set current details
    current_track_id = current_playback["item"]["id"]

    # If current track has changed
    if last_playback and last_track_id != current_track_id:
        last_track_str = f"{last_playback['item']['artists'][0]['name']} - {last_playback['item']['name']}"

        # Read logs.json
        with open("logs.json") as file:
            data = json.load(file)

        # If song is recorded in database, create it
        if not last_track_str in data:
            data[last_track_str] = {}
            data[last_track_str]["plays"] = 0
            data[last_track_str]["status"] = "alive"
        
        # Necessary stuff for each song
        data[last_track_str]["plays"] += 1
        data[last_track_str]["last_played"] = time.strftime('%d/%m/%Y %H:%M')

        # If user wasn't at least 3/4 through song, delete
        if last_progress < last_track_duration * 3/4:
            # Delete song from playlist
            sp.playlist_remove_all_occurrences_of_items(PLAYLIST_ID, [last_track_id])

            # Flag track as dead
            data[last_track_str]["status"] = "killed"

            # Message console that song was killed.
            print(f"Killed '{last_track_str}'.")
         
        else:
            # Message console that song was increment.
            print(f"Incremented '{last_track_str}'.")
        
        # Write data to logs.json
        with open("logs.json", "w") as file:
            json.dump(data, file, indent=2)


    # Set last details
    last_playback = current_playback
    last_track_id = current_track_id
    last_track_duration = current_playback["item"]["duration_ms"]
    last_progress = current_playback["progress_ms"]
