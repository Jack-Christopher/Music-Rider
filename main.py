from functions import *
from pydeezer import Deezer
from dotenv import load_dotenv

load_dotenv()

# You can get your ARL by manually logging into Deezer using your browser check 
# the value of "ARL" in the cookies, finally set the ARL value in the .env file 
arl = os.getenv('ARL')
deezer = Deezer(arl=arl)

set_storage_path()

# menu
while (True):
    os.system("cls")
    print("Options:")
    print("1. Add songs")
    print("2. Add multiple songs from the same artist")
    print("3. Add albums")
    print("4. Add multiple albums from the same artist")
    print("5. Perform download")
    print("6. Exit")

    option = input("Enter your option: ")
    os.system("cls")

    if option == "1":
        add_songs(deezer)
    elif option == "2":
        add_songs_from_same_artist(deezer)
    elif option == "3":
        add_albums(deezer)
    elif option == "4":
        add_albums_from_same_artist(deezer)
    elif option == "5":
        download(deezer)
    elif option == "6":     
        break