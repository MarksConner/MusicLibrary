from storage import Storage
from spotify_api import Spotify
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import os

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_library.json"
        self.mock_spotify = MagicMock()
        self.mock_spotify.search_album.return_value = [{"name": "2014 Forest Hills Drive", "artists": [{"name": "J. Cole"}]}]
        self.storage = Storage(filename="test_library.json")

        with patch("builtins.input", return_value = "1"):
            self.storage.add_album("J. Cole", "2014 Forest Hills Drive")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    #add_album tests
    def test_add_new_artist(self):
        self.assertIn("J. Cole", self.storage.library)
        self.assertIn("Forest Hills Drive", self.storage.library["J. Cole"])

    def test_add_duplicate(self):
            with patch("builtins.input", return_value = "1"):
                self.storage.add_album("J. Cole", "2014 Forest Hills Drive")

            expected_output = "Album already exists for this artist"
            with patch('sys.stdout', new=StringIO()) as fake_out:
                self.storage.total_library()
                self.assertEqual(fake_out.getvalue().strip(), expected_output.strip())

    def test_add_existing_artist(self):
        self.storage.add_album("J. Cole", "Born Sinner")
        self.assertEqual(self.storage.library["J. Cole"], ["Forest Hills Drive", "Born Sinner"])

    def test_multiple(self):
        self.storage.add_album("Pierce the Veil", "Collide with the Sky")
        self.assertIn("J. Cole", self.storage.library)
        self.assertIn("Pierce the Veil", self.storage.library)

    #remove_album tests
    def test_remove(self):
        result = self.storage.remove_album("J. Cole", "Forest Hills Drive")
        self.assertNotIn("J. Cole", self.storage.library)
        self.assertEqual(self.storage.library, {})
        self.assertEqual(result, "Removed '{record}' from {artist}. No more records in {artist}. Removed artist from library.")
    
    def test_remove_nonexisting(self):
        result = self.storage.remove_album("Pierce the Veil", "Collide with The Sky")
        self.assertEqual(result, "Artist does not exist, removal failed.")

    def test_remove_wrong_record(self):
        result = self.storage.remove_album("J. Cole", "Born Sinner")
        self.assertEqual(result, "Record does not exist for this artist, removal failed.")

    def test_remove_multiple(self):
        self.storage.add_album("Pierce the Veil", "Collide with the Sky")
        result = self.storage.remove_album("J. Cole", "Forest Hills Drive")
        self.assertEqual(result, "Removed '{record}' from {artist}. No more records in {artist}. Removed artist from library.")
        self.assertEqual(self.storage.library, {"Pierce the Veil": ["Collide with the Sky"]}) 
    
    def test_remove_same_artist(self):
        self.storage.add_album("J. Cole", "Born Sinner")
        result = self.storage.remove_album("J. Cole", "Born Sinner")
        self.assertEqual(result, "Removed '{record}' from {artist}.")
        self.assertEqual(self.storage.library["J. Cole"], ["Forest Hills Drive"])

    #extra functionalities
    def test_total_library(self):
        self.storage.add_album("J. Cole", "Born Sinner")
        self.storage.add_album("Pierce the Veil", "Collide with the Sky")
        expected_output = "J. Cole: Forest Hills Drive, Born Sinner\nPierce the Veil: Collide with the Sky\n"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.storage.total_library()
            self.assertEqual(fake_out.getvalue().strip(), expected_output.strip())

    def test_total_albums(self):
        self.storage.add_album("J. Cole", "Born Sinner")
        self.storage.add_album("Pierce the Veil", "Collide with the Sky")
        expected_output = "- Forest Hills Drive\n- Born Sinner\n- Collide with the Sky\nTotal records: 3\n"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.storage.total_albums()
            self.assertEqual(fake_out.getvalue().strip(), expected_output.strip())

    def test_total_artists(self):
        self.storage.add_album("J. Cole", "Born Sinner")
        self.storage.add_album("Pierce the Veil", "Collide with the Sky")
        
        expected_output = "\n- J. Cole\n- Pierce the Veil\nTotal number of Artists: 2\n"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.storage.total_artists()
            self.assertEqual(fake_out.getvalue().strip(), expected_output.strip())

if __name__ == '__main__':
    unittest.main()