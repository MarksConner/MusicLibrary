from functions import menu, add, remove, track_search
from storage import Storage
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

class test_functions(unittest.TestCase):

    def setUp(self):
        self.mock_storage = MagicMock()

    def test_menu(self):
        expected_output = (
            "\nVinyl Record Collection\n\n"
            "1. Add an album to your collection.\n"
            "2. Remove an album from your collection.\n"
            "3. Search for a song.\n"
            "4. View total library.\n"
            "0. Exit.\n\n")
        
        with patch("sys.stdout", new=StringIO()) as fake_out:
            menu()
        self.assertEqual(fake_out.getvalue(), expected_output)


    def test_add(self):
        with patch("builtins.input", side_effect=["J. Cole", "2014 Forest Hills Drive", "n"]):
            add(self.mock_storage)
        self.mock_storage.add_album.assert_called_once_with("J. Cole", "2014 Forest Hills Drive")

    def test_add_cancel(self):
        with patch("builtins.input", side_effect=["00"]):
            add(self.mock_storage)
        self.mock_storage.add_album.assert_not_called()



    def test_remove(self):
        with patch("builtins.input", side_effect=["J. Cole", "2014 Forest Hills Drive", "n"]):
            remove(self.mock_storage)
        self.mock_storage.remove_album.assert_called_once_with("J. Cole", "2014 Forest Hills Drive")

    
    def test_remove_cancel(self):
        with patch("builtins.input", side_effect=["00"]):
            remove(self.mock_storage)
        self.mock_storage.remove_album.assert_not_called()
        
    def test_track_search(self):
        self.mock_storage.song.return_value = (None, None)

        with patch("builtins.input", side_effect=["CHIHIRO", "Billie Eilish", "00"]):
            track_search(self.mock_storage)
        self.mock_storage.song.assert_called_once_with("CHIHIRO", "Billie Eilish")


    #integration tests
    def test_add_integrate(self):
        storage = Storage(library={})
        with patch("builtins.input", side_effect=["J. Cole", "2014 Forest Hills Drive", "1", "n"]):
            add(storage)
        self.assertIn("J. Cole", storage.library)
        self.assertIn("2014 Forest Hills Drive", storage.library["J. Cole"])

    def test_remove_integrate(self):
        storage = Storage(library={"J. Cole": ["2014 Forest Hills Drive"]})
        with patch("builtins.input", side_effect=["J. Cole", "2014 Forest Hills Drive", "1", "n"]):
            remove(storage)
        self.assertNotIn("J. Cole", storage.library)

    def test_track_integrate(self):
        storage = Storage(library={"Billie Eilish": ["HIT ME HARD AND SOFT"]})
        storage.song = MagicMock(return_value=("CHIHIRO", "Billie Eilish"))

        storage.spotify.search_song = MagicMock(return_value=[{"album": {"name": "HIT ME HARD AND SOFT"}, "artists": [{"name": "Billie Eilish"}]}])

        with patch("builtins.input", side_effect=["CHIHIRO", "Billie Eilish", "n"]):
            with patch("builtins.print") as mock_print:
                track_search(storage)

        storage.song.assert_called_once_with("CHIHIRO", "Billie Eilish")
        storage.spotify.search_song.assert_called_once_with("CHIHIRO", "Billie Eilish")
        mock_print.assert_any_call("\nCHIHIRO is on HIT ME HARD AND SOFT by Billie Eilish")
        mock_print.assert_any_call("HIT ME HARD AND SOFT is in your collection\n")

if __name__ == '__main__':
    unittest.main()