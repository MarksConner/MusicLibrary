from spotify_api import Spotify
import unittest
from unittest.mock import patch, MagicMock

class test_spotify_api(unittest.TestCase):

    def setUp(self):
        self.spotify = Spotify()
        self.spotify.sp = MagicMock()

    def test_album_search_api(self):
        self.spotify.sp.search.return_value = {"albums": {"items": [{"name": "HIT ME HARD AND SOFT", "artists": [{"name": "Billie Eilish"}]}]}}
        result = self.spotify.search_album("Billie Eilish", "HIT ME HARD AND SOFT")

        self.assertEqual(result[0]["name"], "HIT ME HARD AND SOFT")
        self.assertEqual(result[0]["artists"][0]["name"], "Billie Eilish")
        

    def test_search_album_no_results(self):
        self.spotify.sp.search.return_value = {"albums": {"items": []}}
        result = self.spotify.search_album("zxyu", "")

        self.assertEqual(result, [])

    def test_song_search_api(self):
        self.spotify.sp.search.return_value = {"tracks": {"items": [{"name": "CHIHIRO","artists": [{"name": "Billie Eilish"}]}]}}
        result = self.spotify.search_song("CHIHIRO", "Billie Eilish")

        self.assertEqual(result, [{"name": "CHIHIRO", "artists": [{"name": "Billie Eilish"}]}])

    def test_song_search_no_results(self):
        self.spotify.sp.search.return_value = {"tracks": {"items": []}}
        result = self.spotify.search_song("zxyu", "")

        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()