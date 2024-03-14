'''Рейтинговые треки'''
import fake_useragent, requests
from bs4 import BeautifulSoup

class RatingCount:
    '''
    Функция для получения списка рейтинговых треков с сайта rur.hitmotop.com.
param: count - число от 1 до 48, кол-во треков
\nДля получения информации доступны след.функции:
    - get_author: list, автор трека;
    - get_title: list, название трека;
    - get_url_down: list, ссылка на скачивание трека;
    - direct_download_link: list прямая ссылка на скачивание трека;
    - get_duraction: list, длительность трека;
    - get_picture_url: list, ссылка на обложку трека;
    - get_url_track: list, ссылка на трек.
 
    '''

    def __init__(self, count_tracks, get_redirect_url=False):
        self.count_tracks = count_tracks
        self.get_redirect_url = get_redirect_url
        self.count_selection
    
    @property
    def count_selection(self):
        
        if self.count_tracks >48: 
            raise ValueError('Only <= 48')
        else:
            
            __user = fake_useragent.UserAgent().random
            __headers = {'user-agent': __user}
            __url11= requests.get('https://hitmos.me/', headers=__headers, allow_redirects=True).url
            __url1= __url11[:-1] if '/' in __url11[-1] else __url11

            url = f"{__url1}{'/' if '/' in __url1[:-1] else ''}songs/top-rated"
            
            response = requests.get(url, headers=__headers)
            _soup = BeautifulSoup(response.text, 'html.parser')

            _track_titles = [i.text.strip() for i in _soup.find_all("div", class_="track__title")]
            _track_artists = [i.text.strip() for i in _soup.find_all("div", class_="track__desc")]
            _track_duration = [i.text.strip() for i in _soup.find_all("div", class_="track__fulltime")]
            _track_pictures = [f"{i.get('style')[23:-3]}" for i in _soup.find_all("div", class_="track__img")]
            _track_urls_dow = [i.get('href') for i in _soup.find_all('a', class_='track__download-btn')]
            _track_url = [f"{__url1}{tra_url.get('href')}" for tra_url in _soup.find_all('a', class_='track__info-l')]

            _items = []

            for idx in range(min(len(_track_titles), self.count_tracks)):
                if self.get_redirect_url and len(_track_urls_dow[idx])>0:
                    direct_download_link = requests.get(_track_urls_dow[idx],headers=__headers,allow_redirects=True).url
                else: direct_download_link = None
                item = {
                    'author': _track_artists[idx],
                    'title': _track_titles[idx].replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|','').replace('\\',''),
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
