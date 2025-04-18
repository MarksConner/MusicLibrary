from storage import Storage
import unittest
class TestStorage(unittest.TestCase):
    def setUp(self):
        self.storage = Storage()
        self.storage.add_album("J. Cole", "Forest Hills Drive")

    def tearDown(self):
        del self.storage

    #add_album tests
    def test_add_new_artist(self):
        self.assertIn("J. Cole", self.storage.library)
        self.assertIn("Forest Hills Drive", self.storage.library["J. Cole"])

    def test_add_duplicate(self):
        with self.assertRaises(ValueError):
            self.storage.add_album("J. Cole", "Forest Hills Drive")

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
    def test_total_records(self):
        self.storage.add_album("J. Cole", "Born Sinner")
        self.storage.add_album("Pierce the Veil", "Collide with the Sky")
        self.assertEqual(3, self.storage.total_records())

    def test_total_artists(self):
        self.storage.add_album("J. Cole", "Born Sinner")
        self.storage.add_album("Pierce the Veil", "Collide with the Sky")
        self.assertEqual(2, self.storage.total_artists())

if __name__ == '__main__':
    unittest.main()