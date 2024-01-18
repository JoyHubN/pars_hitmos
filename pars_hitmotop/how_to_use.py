from .entered_tracks import EnteredTrack
import urllib.request, os
from colorama import Fore, Style, init
os.system('cls')
init()

path=r'C:\Users\днс\python_project\pars_hitmotop\music'
result=EnteredTrack('linkin park',10)


# Получить количество треков
amout = result.count_tracks

# Получить автора треков
author = result.get_author
       
# Получить названия треков
title = result.get_title

# Получить ссылки на скачивания треков
url_down= result.get_url_down

# Получить прямую ссылку на скачивание треков
url_down_new= result.direct_download_link

# Получить длителькость треков
duraction = result.get_duraction

# Получить обложки треков
picture = result.get_picture_url

# Получить ссылки на треки
url_tracks = result.get_url_track

# Скачать найденные треки треки    
def down_music(path,result):
    for _ in range(result.count_tracks):
        print(f'Скачиваю по ссылке: {result.direct_download_link[_]}')
        if result.direct_download_link[_] != None:
            urllib.request.urlretrieve(result.direct_download_link[_],f"{path}\{result.get_title[_]}.mp3")
        else:
            print(result.get_title[_])
            print(f'Скачиваю hitmotop\n{result.get_url_down[_]}')
            urllib.request.urlretrieve(result.get_url_down[_],f"{path}\{result.get_title[_]}.mp3")


print(f'{Fore.BLUE+Style.BRIGHT}1 запрос {result.music_name}{Style.RESET_ALL}\n')
for _ in range(result.count_tracks):
    print(f"{author} - {title} {duraction}")
down_music(path, result)


result = EnteredTrack('green day', 10)

print(f'\n\n{Fore.GREEN+Style.BRIGHT}2 запрос {result.music_name}\n\n{Style.RESET_ALL}')
for _ in range(result.count_tracks):
    print(f"{result.get_author} - {result.get_title} {result.get_duraction}")
down_music(path, result)