from storage import Storage
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import os
import json

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_library.json"
        self.mock_spotify = MagicMock()
        self.storage = Storage(filename="test_library.json", spotify=self.mock_spotify)

        self.input_patch = patch("builtins.input", return_value="1")
        self.mock_input = self.input_patch.start()

        self.storage.library = {"J. Cole": ["2014 Forest Hills Drive"]}

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.input_patch.stop()

    #add_album tests
    def test_add_new_artist(self):
        self.assertIn("J. Cole", self.storage.library)
        self.assertIn("2014 Forest Hills Drive", self.storage.library["J. Cole"])

    def test_add_duplicate(self):
        self.mock_spotify.search_album.return_value = [{"name": "2014 Forest Hills Drive", "artists": [{"name": "J. Cole"}]}]
        #for some reason need to mock the spotify search here
        with self.assertRaises(ValueError):
            self.storage.add_album("J. Cole", "2014 Forest Hills Drive")
            

    def test_add_existing_artist(self):
        self.mock_spotify.search_album.return_value = [{"name": "Born Sinner", "artists": [{"name": "J. Cole"}]}]
        self.storage.add_album("J. Cole", "Born Sinner")
        self.assertEqual(self.storage.library["J. Cole"], ["2014 Forest Hills Drive", "Born Sinner"])

    def test_multiple(self):
        self.mock_spotify.search_album.return_value = [{"name": "Collide with the Sky", "artists": [{"name": "Pierce the Veil"}]}]
        #with patch("builtins.input", return_value='1'):
        self.storage.add_album("Pierce the Veil", "Collide with the Sky")

        self.assertIn("J. Cole", self.storage.library)
        self.assertIn("Pierce the Veil", self.storage.library)

    #remove_album tests 
    def test_remove(self):
        self.mock_spotify.search_album.return_value = [{"name": "2014 Forest Hills Drive", "artists": [{"name": "J. Cole"}]}]
        result = self.storage.remove_album("J. Cole", "2014 Forest Hills Drive")
        self.assertNotIn("J. Cole", self.storage.library)
        self.assertEqual(self.storage.library, {})
        self.assertEqual(result, "Removed '2014 Forest Hills Drive' from J. Cole. No more records left for this artist, so they were removed from your library.")
    
    def test_remove_nonexisting(self):
        self.mock_spotify.search_album.return_value = [{"name": "Collide with the Sky", "artists": [{"name": "Pierce the Veil"}]}]
        #with patch("builtins.input", return_value='1'):
        result = self.storage.remove_album("Pierce the Veil", "Collide with The Sky")
        self.assertEqual(result, "Artist 'Pierce the Veil' not found in your library.")

    def test_remove_wrong_record(self):
        self.mock_spotify.search_album.return_value = [{"name": "Born Sinner", "artists": [{"name": "J. Cole"}]}]
        #with patch("builtins.input", return_value='1'):
        result = self.storage.remove_album("J. Cole", "Born Sinner")
        self.assertEqual(result, "Album 'Born Sinner' not found for artist 'J. Cole' in your library.")

    def test_remove_multiple(self):
        self.mock_spotify.search_album.return_value = [{'name': "Collide with the Sky", "artists": [{"name": "Pierce the Veil"}]}]
        #with patch("builtins.input", return_value = '1'):
        self.storage.add_album("Pierce the Veil", "Collide with the Sky")

        self.mock_spotify.search_album.return_value = [{"name": "2014 Forest Hills Drive", "artists": [{"name": "J. Cole"}]}]
        result = self.storage.remove_album("J. Cole", "2014 Forest Hills Drive")
        self.assertEqual(result, "Removed '2014 Forest Hills Drive' from J. Cole. No more records left for this artist, so they were removed from your library.")
        self.assertEqual(self.storage.library, {"Pierce the Veil": ["Collide with the Sky"]}) 
    
    def test_remove_same_artist(self):
        self.mock_spotify.search_album.return_value = [{'name': "Born Sinner", "artists": [{"name": "J. Cole"}]}]
        #with patch("builtins.input", return_value = '1'):
        self.storage.add_album("J. Cole", "Born Sinner")
        
        self.mock_spotify.search_album.return_value = [{"name": "Born Sinner", "artists": [{"name": "J. Cole"}]}]
        #with patch("builtins.input", return_value='1'):
        result = self.storage.remove_album("J. Cole", "Born Sinner")
        self.assertEqual(result, "Removed 'Born Sinner' from J. Cole.")
        self.assertEqual(self.storage.library["J. Cole"], ["2014 Forest Hills Drive"])

    #extra functionalities
    def test_total_library(self):
        self.mock_spotify.search_album.return_value = [{'name': "Born Sinner", "artists": [{"name": "J. Cole"}]}]
        #with patch("builtins.input", return_value = '1'):
        self.storage.add_album("J. Cole", "Born Sinner")
        self.mock_spotify.search_album.return_value = [{'name': "Collide with the Sky", "artists": [{"name": "Pierce the Veil"}]}]
        #with patch("builtins.input", return_value = '1'):
        self.storage.add_album("Pierce the Veil", "Collide with the Sky")
        
        expected_output = "- J. Cole: 2014 Forest Hills Drive, Born Sinner\n- Pierce the Veil: Collide with the Sky\n\nTotal number of Artists: 2\nTotal records: 3"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.storage.total_library()
            self.assertEqual(fake_out.getvalue().strip(), expected_output.strip())

    def test_total_library_empty(self):
        self.mock_spotify.search_album.return_value = [{"name": "2014 Forest Hills Drive", "artists": [{"name": "J. Cole"}]}]
        result = self.storage.remove_album("J. Cole", "2014 Forest Hills Drive")
        
        expected_output = "Library is empty."
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.storage.total_library()
            self.assertEqual(fake_out.getvalue().strip(), expected_output.strip())

    def test_save_to_file(self):
        self.storage.save_to_file()
        with open(self.test_file, 'r') as file:
            data = json.load(file)
        file = {"J. Cole": ["2014 Forest Hills Drive"]}
        self.assertEqual(data, file)

    def test_load_from_file(self):
        self.storage.save_to_file()
        self.library = {}
        self.storage.load_from_file()
        file = {"J. Cole": ["2014 Forest Hills Drive"]}
        self.assertEqual(self.storage.library, file)

    def test_load_file_not_found(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

        self.storage.load_from_file()
        self.assertEqual(self.storage.library, {})

    



class TestSearches(unittest.TestCase):
    def setUp(self):
        self.mock_spotify = MagicMock()
        self.storage = Storage(spotify=self.mock_spotify)
        self.input_patch = patch("builtins.input", return_value="1")
        self.mock_input = self.input_patch.start()

    def tearDown(self):
        self.input_patch.stop()
    #Spotify searches
    def test_album(self):
        self.mock_spotify.search_album.return_value = [{'name': "Born Sinner", "artists": [{"name": "J. Cole"}]}]
        artist, record = self.storage.album("J. Cole", "Born Sinner")
        self.assertEqual(artist, "J. Cole")
        self.assertEqual(record, "Born Sinner")

    def test_no_album_results(self):
        self.mock_spotify.search_album.return_value = []
        artist, record = self.storage.album("zxyu", "")
        self.assertIsNone(artist)
        self.assertIsNone(record)

    def test_song(self):
        self.mock_spotify.search_song.return_value = [{'name': "CHIHIRO", "artists": [{"name": "Billie Eilish"}]}]
        song, artist = self.storage.song("CHIHIRO", "Billie Eilish")
        self.assertEqual(song, "CHIHIRO")
        self.assertEqual(artist, "Billie Eilish")

    def test_no_song_results(self):
        self.mock_spotify.search_album.return_value = []
        song, artist = self.storage.song("zxyu", "")
        self.assertIsNone(song)
        self.assertIsNone(artist)


if __name__ == '__main__':
    unittest.main()