from storage import Storage
#test

#not needed because gui
def menu():
    print("\nVinyl Record Collection\n")
    print("1. Add an album to your collection.")
    print("2. Remove an album from your collection.")
    print("3. Search for a song.")
    print("4. View total library.")
    print("0. Exit.\n")

def add(storage: Storage):
    while True:
        artist = input("What is the artist's name or type '00' to cancel: \n")
        if artist == '00':
            break
        record = input("What is the record's name or type '00' to cancel: \n")
        if record == '00':
            break
        try:
            storage.add_album(artist, record)
        except ValueError as err:
            print(f"Error: {err}")

        clear = input("Add another album? y/n\n")
        if clear.lower() == "y":
            continue
        else:
            break

def remove(storage: Storage):
    while True:
        if not storage.library:
            print("Nothing in your current collection.\n")
            break

        artist_input = input("Enter the artist name or type '00' to cancel: ").strip()
        if artist_input == '00':
            break

        record_input = input("Enter the album name or type '00' to cancel: ").strip()
        if record_input == '00':
            break

        result = storage.remove_album(artist_input, record_input)
        print(result)

        more = input("\nRemove another album? (y/n): ").strip().lower()
        if more != 'y':
            break

def track_search(storage: Storage):
    while True:
        song_input = input("What song would you like to look for? Or 00 to exit: ").strip()
        if song_input == '00':
            break

        artist_input = input("What artist is the song by? Or 00 to exit: ").strip()
        if artist_input == '00':
            break

        song, artist = storage.song(song_input, artist_input)
        if not song or not artist:
            continue
        
        updated_match = storage.spotify.search_song(song, artist)
        selected = updated_match[0]
        album_name = selected['album']['name']
        artist_name = selected['artists'][0]['name']

        print(f"\n{song} is on {album_name} by {artist_name}")
        if artist in storage.library and album_name in storage.library[artist]:
            print(f"{album_name} is in your collection\n")
        else:
            print(f"{album_name} is not in your collection\n")
        
        repeat = input("Search for another song? y/n: ")
        if repeat.lower() != 'y':
            break
        