import os
import json
import music_tag
import urllib.request
from tkinter import Tk, filedialog
from pydeezer.constants import track_formats

def set_storage_path():
    file_path = ""
    # if file data.json soen't exists, create it
    if not os.path.exists('data.json'):
        with open('data.json', 'w') as f:
            json.dump({}, f)

    with open('data.json', 'r') as f:
        data = json.load(f)
        if 'storage_path' not in data or data['storage_path'] == "":
            print("Select the folder where you want to save your music files")
            input("-- press enter to continue...")
            root = Tk() 
            root.withdraw()
            root.attributes('-topmost', True)
            file_path = filedialog.askdirectory(title="Select the path to save the files")
            data = {}
            data['storage_path'] = file_path
            json.dump(data, open('data.json', 'w'), indent=4)
        else:
            file_path = data['storage_path']                        
    return file_path


def add_song(deezer):
    song_name = input("Enter the name of the song: ")
    track_search_results = deezer.search_tracks(song_name)
    song = [None, None]

    song_artist = input("Enter the name of the artist: ")
    artist_search_results = deezer.search_artists(song_artist, limit=1)
    artist_id = artist_search_results[0]['id']

    for i in range(len(track_search_results)):
        if track_search_results[i]['artist']['id'] == artist_id:
            temp = {}
            temp['title'] = track_search_results[i]['title']
            temp['artist_id'] = track_search_results[i]['artist']['id']
            temp['artist_name'] = track_search_results[i]['artist']['name']
            temp['cover'] = track_search_results[i]['album']['cover']
            song[0] = track_search_results[i]['id']
            song[1] = temp
            break
    
    if not os.path.exists('music.json'):
        with open('music.json', 'w') as f:
            json.dump({
                "tracks": { },
                "albums": { }
            }, f)

    with open('music.json', 'r') as f:
        music = json.load(f)
        if str(song[0]) not in music['tracks']:
            music['tracks'][song[0]] = song[1]
            json.dump(music, open('music.json', 'w'), indent=4)
        else:
            print("The song \"" + song[1]['title'] + "\" is already in the list.")


def add_album(deezer):
    album_name = input("Enter the name of the album: ")
    album_search_results = deezer.search_albums(album_name)

    album_artist = input("Enter the name of the artist: ")
    artist_search_results = deezer.search_artists(album_artist, limit=1)
    artist_id = artist_search_results[0]['id']

    album = [None, None]
    for i in range(len(album_search_results)):
        if album_search_results[i]['artist']['id'] == artist_id:
            temp = {}
            temp['title'] = album_search_results[i]['title']
            temp['artist_id'] = album_search_results[i]['artist']['id']
            temp['artist_name'] = album_search_results[i]['artist']['name']
            temp['cover'] = album_search_results[i]['cover']


            album[0] = album_search_results[i]['id']
            album[1] = temp
            break

    with open('music.json', 'r') as f:
        music = json.load(f)
        if str(album[0]) not in music['albums']:
            music['albums'][album[0]] = album[1]
            json.dump(music, open('music.json', 'w'), indent=4)
        else:
            print("The album \"" + album[1]['title'] + "\" is already in the list.")


def download_track(deezer, track_id, track_name, file_path, img_url):
    track = deezer.get_track(track_id)
    track["download"](file_path, quality=track_formats.MP3_320, with_lyrics=False)

    audiofile = music_tag.load_file(file_path+ "/" + track_name + ".mp3")
    urllib.request.urlretrieve(img_url, os.getcwd() + "/images/temp.jpg")
    with open('images/temp.jpg', 'rb') as img_in:
        audiofile['artwork'] = img_in.read()

    audiofile.save()


def download(deezer):
    songs = {"total": 0, "downloaded": 0}
    albums = {"total": 0, "downloaded": 0}
    download_dir = set_storage_path()

    with open('music.json', 'r') as f:
        music = json.load(f)

        for track_id in music['tracks']:
            if not os.path.exists(download_dir + "/" + music['tracks'][track_id]['title'] + ".mp3"):
                download_track(deezer, track_id, music['tracks'][track_id]['title'],download_dir, music['tracks'][track_id]['cover'])
                songs['downloaded'] += 1
                                
        for album_id in music['albums']:
            folder_dir = download_dir + "/" + music['albums'][album_id]['title'] + "/"
            if not os.path.isdir(folder_dir):
                os.mkdir(folder_dir)
                albums['downloaded'] += 1
                album = deezer.get_album(album_id)
                for i in album['tracks']['data']:
                    if not os.path.exists(folder_dir + i['title'] + ".mp3"):
                        download_track(deezer, i['id'], i['title'],folder_dir, music['albums'][album_id]['cover'])
                        songs['downloaded'] += 1

    
    songs['total'] = sum(len(files) for _, _, files in os.walk(download_dir))
    albums['total'] = len(next(os.walk(download_dir))[1])
    print("Downloaded songs: " + str(songs['downloaded']))
    print("Total songs: " + str(songs['total']))
    print("Downloaded albums : " + str(albums['downloaded']))
    print("Total albums: " + str(albums['total']))
    input("press enter to exit...")