import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def extract_track_details(uri):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    results = sp.track(uri)
    artists = results['artists']
    name = results['name']
    album_name = results['album']['name']
    return {"artists": artists, "name": name, "album_name": album_name}