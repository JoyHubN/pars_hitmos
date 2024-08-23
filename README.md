# Оглавление
0. [Оглавление](https://github.com/PY079/pars_hitmotop#оглавление)
1. [Что именно парсит?](https://github.com/PY079/pars_hitmotop/blob/main/README.md#что-именно-парсит)
2. [Как использовать модуль entered_tracks](https://github.com/PY079/pars_hitmotop/blob/main/README.md#как-использовать-модуль-entered_tracks)
3. [Как использовать модуль rating_tracks_count](https://github.com/PY079/pars_hitmotop/blob/main/README.md#как-использовать-модуль-rating_tracks_count)
4. [Как использовать модуль rating_tracks_page](https://github.com/PY079/pars_hitmotop/blob/main/README.md#как-использовать-модуль-rating_tracks_page)
5. [Что можно достать при запросе?](https://github.com/PY079/pars_hitmotop/blob/main/README.md#что-можно-достать-при-запросе)
____
Этот проект парсит [музыкальный сайт](https://hitmos.me/)
____
# Что именно парсит?
1. [Рейтинговые треки](https://hitmos.me/songs/top-rated) от 1 до 48;
2. Тоже [рейтинговые треки](https://hitmos.me/songs/top-rated) но можно выбрать количество страниц, с которых будет произведен парсинг;
3. Треки введенные пользователем. Парсит от 1 трека до конечной страницы (на одной странице 48 треков)
____
## Как использовать модуль *entered_tracks*
```
from pars_hitmotop.entered_tracks import EnteredTrack
result=EnteredTrack('linkin park',10)
```
1 аргументом (music_name) передается название песни или автора. 2 Аргументом (count) передается количество треков
____
## Как использовать модуль *rating_tracks_count*
```
from pars_hitmotop.rating_tracks_count import RatingCount
result=RatingCount(10)
```
1 аргументом (count) передается количество песен
____
## Как использовать модуль *rating_tracks_page*
```
from pars_hitmotop.rating_tracks_page import RatingPage
result=RatingPage(10)
```
1 аргументом (count) передается количество страниц (max 11)
____
# Что можно достать при запросе?
Все возвращается в виде list
| Метод | Описание |
|----------------|:---------|
| result.get_author | Получить автора трека|
|result.get_title| Получить название трека|
|result.get_url_down|Получить ссылку на скачивание трека|
|result.direct_download_link|Получить прямую ссылку на скачивание трека|
|result.get_duration|Получить продолжительность трека|
|result.get_picture_url|Получить ссылку на обложку трека|
|result.get_url_track|Получить ссылку трек|
|result.get_all|Получить все данные в виде словаря|
|result.get_author_title|Получить лист в виде автор - название|

____
