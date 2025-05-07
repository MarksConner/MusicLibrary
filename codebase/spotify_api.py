#from dotenv import load_dotenv
#load_dotenv()

#import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class Spotify:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            #client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            #client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
            client_id=("1df1e40772b54399a5715ebd130c4f6b"),
            client_secret=("c4ea73b5adc145bc974af1f8f07ee44b")
        ))

    def search_album(self, artist: str, album: str, limit: int = 5):
        query = f"album:{album} artist:{artist}"
        results = self.sp.search(q=query, type="album", limit=limit)
        return results["albums"]["items"]

    def search_song(self, song: str, artist: str, limit: int = 5):
        query = f"track:{song} artist:{artist}"
        results = self.sp.search(q=query, type="track", limit=limit)
        return results["tracks"]["items"]
