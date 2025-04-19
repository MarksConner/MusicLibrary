import spotipy
from spotipy.oauth2 import SpotifyOAuth

class Spotify:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="1df1e40772b54399a5715ebd130c4f6b",
            client_secret="c4ea73b5adc145bc974af1f8f07ee44b",
            redirect_uri="http://127.0.0.1:8888/callback",
            scope="user-library-read"
        ))


    def search_album(self, artist: str, album: str, limit: int = 5):
        query = f"album:{album} artist:{artist}"
        results = self.sp.search(q=query, type="album", limit=limit)
        return results["albums"]["items"]

    '''def search_album(self, artist: str, album: str):
        query = f"album:{album} artist:{artist}"
        results = self.sp.search(q=query, type="album", limit=5)
        matches = []

        for item in results["albums"]["items"]:
            if artist.lower() in item["artists"][0]["name"].lower() and album.lower() in item["name"].lower():
                matches.append(item)
        if matches:
            return matches[0]
        return None'''