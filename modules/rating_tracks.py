'''Рейтинговые треки'''
import fake_useragent, requests
from bs4 import BeautifulSoup
from excepts import PageError


class rating_tr_48():
    '''
    Функция для получения списка треков с сайта rur.hitmotop.com.
Параметры:
    - page_number: число от 1 до 11, номер страницы с треками
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
    def __init__(self, page_number:int):
        self.page_number = page_number
        self.page_selection

    @property
    def page_selection(self):
 
        if self.page_number >12: 
            raise PageError
        else:
            
            __user = fake_useragent.UserAgent().random
            __headers = {'user-agent': __user}
            if self.page_number == 1:
                __list = []
                url = 'https://rur.hitmotop.com/songs/top-rated'
                response = requests.get(url, headers=__headers)
                _soup = BeautifulSoup(response.text, 'lxml')
                
                _track_titles = [i.text.strip() for i in _soup.find_all("div", class_="track__title")]
                _track_artists = [i.text.strip() for i in _soup.find_all("div", class_="track__desc")]
                _track_duration = [i.text.strip() for i in _soup.find_all("div", class_="track__fulltime")]
                _track_pictures = [f"{i.get('style')[23:-3]}" for i in _soup.find_all("div", class_="track__img")]
                _track_urls_dow = [i.get('href') for i in _soup.find_all('a', class_='track__download-btn')]
                _track_url = [f"https://rur.hitmotop.com{tra_url.get('href')}" for tra_url in _soup.find_all('a', class_='track__info-l')]
                
                for idx in range(min(len(_track_titles), 48)):
                    items={
                        'author': _track_artists[idx],
                        'title': _track_titles[idx],
                        'url_down': _track_urls_dow[idx],
                        'direct_download_link': f"https://ds.cdn1.deliciouspeaches.com/get/music{_track_urls_dow[idx].split('music')[1]}",
                        'url_track': _track_url[idx],
                        'duration_track': _track_duration[idx],
                        'picture_url': _track_pictures[idx]
                    }
                    __list.append(items)
                
                self.count_tracks = len(__list)
                self.data = {'items': __list}
                return self.data
                
            
            else: 
                self.page_number *= 48

                __list = []

                url = 'https://rur.hitmotop.com/songs/top-rated/start/'

                items = []
                for page in range(0, self.page_number, 48):

                    response = requests.get(f'{url}{page}', headers=__headers)
                    soup = BeautifulSoup(response.text, 'lxml')

                    track_titles = [i.text.strip() for i in soup.find_all("div", class_="track__title")]
                    track_artists = [i.text.strip() for i in soup.find_all("div", class_="track__desc")]
                    track_duration = [i.text.strip() for i in soup.find_all("div", class_="track__fulltime")]
                    track_pictures = [f"https://rur.hitmotop.com{i.get('style')[23:-3]}" for i in soup.find_all("div", class_="track__img")]
                    track_urls_dow = [f"{track_dow_url.get('href')}" for track_dow_url in soup.find_all('a', class_='track__download-btn')]
                    track_url = [f"https://rur.hitmotop.com{tra_url.get('href')}" for tra_url in soup.find_all('a', class_='track__info-l')]

                    

                    for idx in range(min(len(track_titles), 48)):
                        if len(track_urls_dow[idx])>0:
                            direct_download_link= f"https://ds.cdn1.deliciouspeaches.com/get/music{track_urls_dow[idx].split('music')[1]}"
                        else: direct_download_link=None
   
                        items={
                            'author': track_artists[idx],
                            'title': track_titles[idx],
                            'url_down': track_urls_dow[idx],
                            'direct_download_link': direct_download_link,
                            'url_track': track_url[idx],
                            'duration_track': track_duration[idx],
                            'picture_url': track_pictures[idx]
                        }
                        __list.append(items)
                self.count_tracks = len(__list)
                self.data = {'items': __list}
                return self.data

    @property
    def get_author(self):
        return [item['author'] for item in self.data['items']]    
    
    @property
    def get_title(self):
        return [item['title'] for item in self.data['items']]
    
    @property
    def get_url_down(self):
        return [item['url_down'] for item in self.data['items']]

    @property
    def direct_download_link(self):
        return [item['direct_download_link'] for item in self.data['items']]

    @property
    def get_duraction(self):
        return [item['duration_track'] for item in self.data['items']]
    
    @property
    def get_picture_url(self):
        return [item['picture_url'] for item in self.data['items']]
    
    @property
    def get_url_track(self):
        return [item['url_track'] for item in self.data['items']]

    @property
    def get_all(self): return self.data
        


