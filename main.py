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
    print("1. Add a song")
    print("2. Add an album")
    print("3. Perform download")
    print("4. Exit")

    option = input("Enter your option: ")

    if option == "1":
        add_song(deezer)
    elif option == "2":
        add_album(deezer)
    elif option == "3":
        os.system("cls")
        download(deezer)
    elif option == "4":
        break