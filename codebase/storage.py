from spotipy.oauth2 import SpotifyOAuth
from typing import Dict, List, Optional, Tuple
import json
from spotify_api import Spotify

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
    #Functions to search through spotify's api
    def album(self, artist: str, record: str) -> Tuple[str, str]:
        if not self.spotify:
            return None, None

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
        
    def song(self, song: str, artist: str) -> Tuple[str, str]:
        if not self.spotify:
            return None, None
        matches = self.spotify.search_song(song, artist)
        if not matches:
            print("No song with this name is found on Spotify.")
            return None, None
        
        print("\nMatching songs:")
        for i, song_matches in enumerate(matches):
            song_name = song_matches["name"]
            artist_name = song_matches["artists"][0]["name"]
            print(f"{i + 1}. {song_name} by {artist_name}")
        
        try:
            choice = int(input("Enter the number of the correct song or type 0 to cancel: ")) - 1
            if choice < 0 or choice >= len(matches[:5]):
                return None, None
            selected = matches[choice]
            song = selected['name']
            artist = selected['artists'][0]['name']
            return song, artist
        except (ValueError, IndexError):
            print("Invalid input")
            return None, None

#----------------------------------------------------------------------------------------------#
    #functionalities
    def add_album(self, artist: str, record: str) -> None:
        #spotify checking for partial mathes
        artist, record = self.album(artist, record)
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
        artist, record = self.album(artist, record)
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
        print("\n")
        for artist, albums in self._library.items():
            album_list = ", ".join(albums)
            print(f"- {artist}: {album_list}")
        print("\nTotal number of Artists:", len(self._library))
        print("Total records:", sum(len(albums) for albums in self._library.values()))

    