import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import Dict, List, Optional
import json
from spotify_api import Spotify
import difflib

class Storage:
    def __init__(self, library: Optional[Dict[str, List[str]]] = None, filename: str = "library.json", spotify = None) -> None:
        self._filename = filename
        self._library: Dict[str, List[str]] = {}
        self.spotify = spotify if spotify else Spotify()
        if library is None:
            self._library: Dict[str, List[str]] = {}
            self.load_from_file()
        else:
            self._library = library

#----------------------------------------------------------------------------------------------#
    #File IO stuff
    def save_to_file(self) -> None:
        try:
            with open(self._filename, 'w') as file:
                json.dump(self._library, file, indent=2)

        except Exception as err:
            print(f"Error saving to file: {err}")

    def load_from_file(self) -> None:
        try:
            with open(self._filename, 'r') as file:
                self._library = json.load(file)

        except FileNotFoundError:
            self._library = {}
        except json.JSONDecodeError:
            print("Library file is corrupted. Creating a new library.")
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
    #Function to search through spotify's api
    def spotify_search(self, artist: str, record: str):
        if not self.spotify:
            return None, None  # Or optionally raise an error

        matches = self.spotify.search_album(artist, record)
        if not matches:
            print("No album with this name is found on Spotify.")
            return None, None

        print("\nMatching albums:")
        for i, album in enumerate(matches[:5]):
            name = album['name']
            artist_name = album['artists'][0]['name']
            print(f"{i + 1}. {name} by {artist_name}")

        try:
            choice = int(input("Enter the number of the correct album or type 0 to cancel: ")) - 1
            if choice < 0 or choice >= len(matches[:5]):
                return None, None
            selected = matches[choice]
            artist = selected['artists'][0]['name']
            record = selected['name']
            return artist, record
        except (ValueError, IndexError):
            print("Invalid input.")
            return None, None

#----------------------------------------------------------------------------------------------#
    #functionalities
    def add_album(self, artist: str, record: str) -> None:
        #spotify checking for partial mathes
        artist, record = self.spotify_search(artist, record)
        if not artist or not record:
            return
            
        #adding the album
        if artist in self._library:
            if record in self._library[artist]:
                raise ValueError("Album already exists for this artist")
            self._library[artist].append(record)
        else:
            self._library[artist] = [record]
        self.save_to_file()
    
    def remove_album(self, artist: str, record: str) -> str:
        artist, record = self.spotify_search(artist, record)
        if not artist or not record:
            return "Cancelled."

        if artist not in self.library:
            return f"Artist '{artist}' not found in your library."

        if record not in self.library[artist]:
            return f"Album '{record}' not found for artist '{artist}' in your library."

        if len(self.library[artist]) > 1:
            self.library[artist].remove(record)
            self.save_to_file()
            return f"Removed '{record}' from {artist}."
        else:
            del self.library[artist]
            self.save_to_file()
            return f"Removed '{record}' from {artist}. No more records left for this artist, so they were removed from your library."

        
    def total_library(self) -> None:
        if not self._library:
            print("Library is empty.")
            return

        for artist, albums in self._library.items():
            album_list = ", ".join(albums)
            print(f"{artist}: {album_list}")
    
    def total_albums(self) -> None:
        print("\n")
        for albums in self._library.values():
            for album in albums:
                print(f"- {album}")
        print("Total records:", sum(len(albums) for albums in self._library.values()))
    
    def total_artists(self) -> None:
        print("\n")
        for artist in self._library.keys():
            print(f"- {artist}")
        print("Total number of Artists:", len(self._library))
    
    #find songs on albums with a music api