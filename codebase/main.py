from storage import Storage
from functions import menu, add, remove, track_search
from spotify_api import Spotify

def main():
    spotify = Spotify()
    storage = Storage(spotify=spotify)
    
    while True:
        menu()
        option = input("Select an option: ")

        match option:
            case "1":
                add(storage)
            
            case "2":
                remove(storage)

            case "3":
                track_search(storage)

            case "4":
                storage.total_library()

            case "0":
                break

            case _:
                print("Invalid option.")


if __name__ == '__main__':
    main()


