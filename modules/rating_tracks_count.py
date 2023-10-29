'''Рейтинговые треки'''
import fake_useragent, requests
from bs4 import BeautifulSoup

class rating_tr_count:
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

    def __init__(self, count_tracks) -> None:
        self.count_tracks = count_tracks
        self.count_selection
    
    @property
    def count_selection(self):
        
        if self.count_tracks >48: 
            raise ValueError('Only <= 48')
        else:
            
            __user = fake_useragent.UserAgent().random
            __headers = {'user-agent': __user}

            url = 'https://rur.hitmotop.com/songs/top-rated'
            response = requests.get(url, headers=__headers)
            _soup = BeautifulSoup(response.text, 'lxml')

            _track_titles = [i.text.strip() for i in _soup.find_all("div", class_="track__title")]
            _track_artists = [i.text.strip() for i in _soup.find_all("div", class_="track__desc")]
            _track_duration = [i.text.strip() for i in _soup.find_all("div", class_="track__fulltime")]
            _track_pictures = [f"{i.get('style')[23:-3]}" for i in _soup.find_all("div", class_="track__img")]
            _track_urls_dow = [i.get('href') for i in _soup.find_all('a', class_='track__download-btn')]
            _track_url = [f"https://rur.hitmotop.com{tra_url.get('href')}" for tra_url in _soup.find_all('a', class_='track__info-l')]

            _items = []

            for idx in range(min(len(_track_titles), self.count_tracks)):
                if len(_track_urls_dow[idx])>0:
                    direct_download_link =  f"https://ds.cdn1.deliciouspeaches.com/get/music{_track_urls_dow[idx].split('music')[1]}"
                else: direct_download_link = None
                item = {
                    'author': _track_artists[idx],
                    'title': _track_titles[idx],
                    'url_down': _track_urls_dow[idx],
                    'direct_download_link': direct_download_link,
                    'duration_track': _track_duration[idx],
                    'picture_url': _track_pictures[idx],
                    'url_track': _track_url[idx]
                }
                _items.append(item)

            self.data = {"items": _items}
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


rt = rating_tr_count(10)
for i in range(rt.count_tracks):
# print(len(rt.get_all['items']), rt.count_tracks)
    print(f'{rt.get_author[i]} - {rt.get_title[i]}')