import fake_useragent
import requests
from bs4 import BeautifulSoup

class RatingTracks:
    @staticmethod
    def get_tracks(count):
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
        
        user_agent = fake_useragent.UserAgent().random
        headers = {'user-agent': user_agent}
        track_list = []

        url = 'https://rur.hitmotop.com/songs/top-rated'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        track_desc = soup.find_all('div', class_='track__desc')
        track_title = soup.find_all('div', class_='track__title')
        track_fulltime = soup.find_all('div', class_='track__fulltime')
        track_img = soup.find_all('div', class_='track__img')
        track_info_l = soup.find_all('a', class_='track__info-l')
        track_download_btn = soup.find_all('a', class_='track__download-btn')

        for i in range(min(count, len(track_desc))):
            picture_style = track_img[i].get('style')
            picture_url = f'https://rur.hitmotop.com{picture_style[23:-3]}'
            item = {
                'author': track_desc[i].text.strip(),
                'title': track_title[i].text.strip(),
                'url_track': f'https://rur.hitmotop.com{track_info_l[i].get("href").strip()}',
                'url_down': track_download_btn[i].get("href").strip(),
                'duration_track': track_fulltime[i].text.strip(),
                'picture_url': picture_url
            }
            track_list.append(item)

        return {'response': {'items': track_list}}
