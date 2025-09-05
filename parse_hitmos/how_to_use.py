import sys, os, urllib.request, pathlib
from parse_hitmos import EnteredTrack, RatingPage, RatingCount
from parse_hitmos.tools.headers import get_headers

def downl(url, info):
    req = urllib.request.Request(url, headers=get_headers())
    with urllib.request.urlopen(req) as response, open(f'{PATH_DOWNLOAD_MUSIC}/{info}.mp3', "wb") as f:
        f.write(response.read())

cwd = pathlib.Path.cwd()
PATH_DOWNLOAD_MUSIC = pathlib.Path.joinpath(cwd, 'download_music')

if not os.path.isdir(PATH_DOWNLOAD_MUSIC): os.mkdir(PATH_DOWNLOAD_MUSIC)

result_entered_tracks = EnteredTrack('linkin park', 10, True)
result_rating_count = RatingCount(1, True)
result_rating_page = RatingPage(1, True)

def print_new_line():
    print('\n------------------------\n')


# Получить количество треков
amount_ET = result_entered_tracks.count_tracks
amount_RC = result_rating_count.count_tracks
amount_RP = result_rating_page.count_tracks

print(f'{amount_ET=}\n{amount_RC=}\n{amount_RP=}\n')
print_new_line()

# Получить автора треков
author_ET = result_entered_tracks.get_author
author_RC = result_rating_count.get_author
author_RP = result_rating_page.get_author

print(f'{author_ET=}\n{author_RC=}\n{author_RP=}\n')
print_new_line()

# Получить названия треков
title_ET = result_entered_tracks.get_title
title_RC = result_rating_count.get_title
title_RP = result_rating_page.get_title

print(f'{title_ET=}\n{title_RC=}\n{title_RP=}\n')
print_new_line()


# Получить ссылки на скачивания треков
url_down_ET = result_entered_tracks.get_url_down
url_down_RC = result_rating_count.get_url_down
url_down_RP = result_rating_page.get_url_down

print(f'{url_down_ET=}\n{url_down_RC=}\n{url_down_RP=}\n')
print_new_line()

# Получить прямую ссылку на скачивание треков
url_down_dir_ET = result_entered_tracks.direct_download_link
url_down_dir_RC = result_rating_count.direct_download_link
url_down_dir_RP = result_rating_page.direct_download_link

print(f'{url_down_dir_ET=}\n{url_down_dir_RC=}\n{url_down_dir_RP=}\n')
print_new_line()

# Получить длительность треков
duration_ET = result_entered_tracks.get_duration
duration_RC = result_rating_count.get_duration
duration_RP = result_rating_page.get_duration

print(f'{duration_ET=}\n{duration_RC=}\n{duration_RP=}\n')
print_new_line()

# Получить обложки треков
picture_ET = result_entered_tracks.get_picture_url
picture_RC = result_rating_count.get_picture_url
picture_RP = result_rating_page.get_picture_url

print(f'{picture_ET=}\n{picture_RC=}\n{picture_RP=}\n')
print_new_line()

# Получить ссылки на треки
url_tracks_ET = result_entered_tracks.get_url_track
url_tracks_RC = result_rating_count.get_url_track
url_tracks_RP = result_rating_page.get_url_track

print(f'{url_tracks_ET=}\n{url_tracks_RC=}\n{url_tracks_RP=}\n')
print_new_line()


# Получить все данные
all_data_ET = result_entered_tracks.get_all
all_data_RC = result_rating_count.get_all
all_data_RP = result_rating_page.get_all

print(f'{all_data_ET=}\n{all_data_RC=}\n{all_data_RP=}\n')
print_new_line()


# Получить автор - название
info_ET = result_entered_tracks.get_author_title
info_RC = result_rating_count.get_author_title
info_RP = result_rating_page.get_author_title

print(f'{info_ET=}\n{info_RC=}\n{info_RP=}\n')
print_new_line()

# Скачать найденные треки треки    
def down_music_ET():
    for _ in range(amount_ET):
        
        if url_down_dir_ET[_] != None:
            print(info_ET[_])
            print(f'Скачиваю по ссылке: {url_down_dir_ET[_]}')
            downl(url_down_dir_ET[_], info_ET[_])
        
        else:
            print(title_ET[_])
            print(f'Скачиваю hitmotop\n{url_tracks_ET[_]}')
            downl(url_tracks_ET[_], info_ET[_])

def down_music_RC():
    for _ in range(amount_RC):
        
        if url_down_dir_RC[_] != None:
            print(info_RC[_])
            print(f'Скачиваю по ссылке: {url_down_dir_RC[_]}')
            downl(url_down_dir_RC[_], info_RC[_])
        
        else:
            print(title_RC[_])
            print(f'Скачиваю hitmotop\n{url_tracks_RC[_]}')
            downl(url_tracks_RC[_], info_RC[_])

def down_music_RP():
    for _ in range(amount_RP):
        
        if url_down_dir_RP[_] != None:
            print(info_RP[_])
            print(f'Скачиваю по ссылке: {url_down_dir_RP[_]}')
            downl(url_down_dir_RP[_], info_RP[_])
        
        else:
            print(title_RP[_])
            print(f'Скачиваю hitmotop\n{url_tracks_RP[_]}')
            downl(url_tracks_RP[_], info_RP[_])


print_new_line()
down_music_ET()
print_new_line()
down_music_RC()
print_new_line()
down_music_RP()
