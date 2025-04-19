from storage import Storage

#not needed because gui
def menu():
    print("\nVinyl Record Collection\n")
    print("1. Add an album to your collection.")
    print("2. Remove an album from your collection.")
    print("3. View total library")
    print("4. View total number of artists in your collection.")
    print("5. View total number of records in your collection.")
    print("0. Exit.\n")

def add(storage: Storage):
    while True:
        artist = input("What is the artist's name?\n")
        record = input("What is the record's name?\n")
        try:
            storage.add_album(artist, record)
        except ValueError as err:
            print(f"Error: {err}")

        clear = input("Add another album? y/n\n")
        if clear.lower() == "n":
            break
        elif clear.lower() == "y":
            continue

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
