from typing import Dict, List, Optional

class Storage:
    def __init__(self, library: Optional[Dict[str, List[str]]] = None) -> None:
        if library is None:
            library = {}
        self._library: Dict[str, List[str]] = library

    @property
    def library(self) -> Dict[str, List[str]]:
        return self._library

    @library.setter
    def library(self, new_library: Dict[str, List[str]]) -> None:
        if isinstance(new_library, dict):
            self._library = new_library
        else:
            raise ValueError("Library must be a dictionary")

    
    def add_album(self, artist: str, record: str) -> None:
        if artist in self.library:
            if record in self.library[artist]:
                raise ValueError("Album already exists for this artist")
            self.library[artist].append(record)
        else:
            self.library[artist] = [record]
    
    def remove_album(self, artist: str, record: str) -> bool:
        if artist not in self.library:
            print("Artist does not exist")
            return False
        if record not in self.library[artist]:
            print("Record does not exist for this artist")
            return False
    
        if len(self.library[artist]) > 1:
            self.library[artist].remove(record)
            print(f"Removed '{record}' from {artist}.")
        else:
            del self.library[artist]
            print(f"Removed '{record}' from {artist}.")
            print(f"No more records in {artist}. Removed artist from library.")
        return True
    
    def total_records(self) -> int:
        return sum(len(albums) for albums in self._library.values())
    
    def total_artists(self):
        return len(self._library)
    
    def save_to_file(self, filename: str) -> None:
        pass
    def load_from_file(self, filename: str) -> None:
        pass
    def search_by_artist(artist_name: str) -> None:#with partial matching
        pass
    def search_by_album(album_name: str) -> None:#with partial matching
        pass
    #find songs on albums with a music api