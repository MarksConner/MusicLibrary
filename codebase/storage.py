from typing import Dict, List, Optional
import json
class Storage:
    def __init__(self, filename: str = "library.json") -> None:
        self._filename = filename
        self._library: Dict[str, List[str]] = {}
        self.load_from_file()

#----------------------------------------------------------------------------------------------#
    #File IO stuff
    def save_to_file(self) -> None:
        try:
            with open(self._filename, 'w') as file:
                json.dump(self._library, file, indent=4)
        except Exception as e:
            print(f"Error saving to file: {e}")

    def load_from_file(self) -> None:
        try:
            with open(self._filename, 'r') as file:
                self._library = json.load(file)
        except FileNotFoundError:
            self._library = {}
        except json.JSONDecodeError:
            print("Library file is corrupted. Starting with an empty library.")
            self._library = {}
    
#----------------------------------------------------------------------------------------------#
    #getters and setters
    @property
    def library(self) -> Dict[str, List[str]]:
        return self._library

    @library.setter
    def library(self, new_library: Dict[str, List[str]]) -> None:
        if isinstance(new_library, dict):
            self._library = new_library
        else:
            raise ValueError("Library must be a dictionary")


#----------------------------------------------------------------------------------------------#
    #functionalities
    def add_album(self, artist: str, record: str) -> None:
        if artist in self.library:
            if record in self.library[artist]:
                raise ValueError("Album already exists for this artist")
            self._library[artist].append(record)
        else:
            self._library[artist] = [record]
        #self.save_to_file()
    
    def remove_album(self, artist: str, record: str) -> str:
        if artist not in self.library:
            return "Artist does not exist, removal failed."
        if record not in self.library[artist]:
            return "Record does not exist for this artist, removal failed."
    
        if len(self.library[artist]) > 1:
            self.library[artist].remove(record)
            return "Removed '{record}' from {artist}."
        else:
            del self.library[artist]
            return "Removed '{record}' from {artist}. No more records in {artist}. Removed artist from library."
        #self.save_to_file()
    
    def total_records(self) -> int:
        return sum(len(albums) for albums in self._library.values())
    
    def total_artists(self):
        return len(self._library)
    
    def search_by_artist(artist_name: str) -> None:#with partial matching
        pass
    def search_by_album(album_name: str) -> None:#with partial matching
        pass
    #find songs on albums with a music api