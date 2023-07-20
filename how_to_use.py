from entered_tracks import Entered_Track_48
import urllib.request, os
os.system('cls')

path='ПУТЬ'




# Получить автора трека/ов
def get_author_track():
    for tracks in mus['response']['items']:
        print(tracks['author'])
       
# Получить названия трекa/ов
def get_title_track():
    for tracks in mus['response']['items']:
        print(tracks['title'])


# Получить ссылку/и на скачивания трека/ов
def get_url_down_track():
    for tracks in mus['response']['items']:
        print(tracks['url_down'])

# Получить длителькость трека/ов
def get_duration_track():
    for tracks in mus['response']['items']:
        print(tracks['duration_track'])

# Получить обложку/и трека/ов
def get_picture_url_track():
    for tracks in mus['response']['items']:
        print(tracks['picture_url'])

# Получить ссылку/и на трек/и
def get_url_track():
    for tracks in mus['response']['items']:
        print(tracks['url_track'])

# Скачать найденные треки треки    
def down_music(path):
    for tracks in mus['response']['items']:
        print(tracks['url_down'])
        urllib.request.urlretrieve(tracks['url_down'],f"{path}{tracks['title']}.mp3")



mus = Entered_Track_48.get('johan x goddamn',10)

for track in mus['response']['items']:
    print(f"{track['author']} - {track['title']} {track['duration_track']}")

mus2 = Entered_Track_48.get('green day',10)
for track in mus2['response']['items']:
    print(f"{track['author']} - {track['title']} {track['duration_track']}")