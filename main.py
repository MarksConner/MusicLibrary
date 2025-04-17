from storage import Storage

def menu():
    print("\nVinyl Record Collection\n")
    print("1. Add an album to your collection.")
    print("2. Remove an album from your collection.")
    print("3. View total library")
    print("4. View total number of records in your collection.")
    print("5. View total number of artists in your collection.")
    print("0. Exit.")

def add(storage: Storage):
    artist = ("What is the artist's name?")
    record = ("What is the record's name?")
    storage.add_album(artist, record)

def main():
    storage = Storage()
    while True:
        menu()
        option = ("Select an option: ")

        match option:
            case 1:
                pass


if __name__ == '__main__':
    main()