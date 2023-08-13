import fake_useragent
import requests
from bs4 import BeautifulSoup
from itertools import islice

class RatingTracks:
    def __init__(self, count: int):
        self.count = count
    
    @staticmethod
    def get_tracks(count: int):
        '''
        Функция для получения списка треков с сайта rur.hitmotop.com.
        Параметры:
        - count: число от 1 до 48, кол-во треков
        Возвращает словарь вида:
        {'response': {'items': [...]}} - список словарей с информацией о каждом треке.
        \nСловарь о треке содержит следующие ключи:
        - 'author': автор трека
        - 'title': название трека
        - 'url_track': ссылка на страницу с треком
        - 'url_down': ссылка на скачивание трека
        - 'duration_track': длительность трека
        - 'picture_url': ссылка на обложку трека
        '''
        if count > 48: 
            raise ValueError('Only <= 48')

        else:
        
            __user_agent = fake_useragent.UserAgent().random
            __headers = {'user-agent': __user_agent}
            

            __url = 'https://rur.hitmotop.com/songs/top-rated'
            __response = requests.get(__url, headers=__headers)
            __soup = BeautifulSoup(__response.text, 'lxml')

            __track_info = zip(
                __soup.find_all('div', class_='track__desc'),
                __soup.find_all('div', class_='track__title'),
                __soup.find_all('div', class_='track__fulltime'),
                __soup.find_all('div', class_='track__img'),
                __soup.find_all('a', class_='track__info-l'),
                __soup.find_all('a', class_='track__download-btn')
            )

            __track_list = []
            for track_artist, track_title, duration, picture_style, url_track, url_download in islice(__track_info, count):
                picture_url = f'https://rur.hitmotop.com{picture_style.get("style")[23:-3]}'
                __item = {
                    'author': track_artist.text.strip(),
                    'title': track_title.text.strip(),
                    'url_track': f'https://rur.hitmotop.com{url_track.get("href").strip()}',
                    'url_down': url_download.get("href").strip(),
                    'duration_track': duration.text.strip(),
                    'picture_url': picture_url
                }
                __track_list.append(__item)

            return {'response': {'items': __track_list}}
