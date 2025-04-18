from storage import Storage
from functions import menu, add, remove

def main():
    storage = Storage()
    
    while True:
        menu()
        option = input("Select an option: ")

        match option:
            case "1":
                add(storage)
            
            case "2":
                remove(storage)

            case "3":
                pass
            case "4":
                print(storage.total_records())
            case "5":
                pass
            case "0":
                break

            case _:
                print("Invalid option.")


if __name__ == '__main__':
    main()


