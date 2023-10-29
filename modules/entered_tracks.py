import fake_useragent, requests
from bs4 import BeautifulSoup
from modules.excepts import NoFoundTrack, MaxTrack
'''Треки из переданного запроса'''



class Entered_Track_48:
    """
:param music_name: Название и автор трека в одной строке.
:type music_name: str
:param amount: Количество треков, которое нужно вывести. Max 48.
:type amount: int
:return: Список словарей с информацией о треках. Каждый словарь содержит следующие поля:
    - 'author': str, автор трека;
    - 'title': str, название трека;
    - 'url_down': str, ссылка на скачивание трека;
    - 'duration_track': str, длительность трека;
    - 'picture_url': str, ссылка на обложку трека;
    - 'url_track': str, ссылка на страницу трека.
 
    """

    def __init__(self, music_name:str, amount:int, get_redirect_url=False):
        self.music_name = music_name
        self.amount = amount
        self.get_redirect_url = get_redirect_url
        self.get_2
        

    @property
    def get_2(self):

        if self.amount > 48:
            raise MaxTrack
        else:
            __user = fake_useragent.UserAgent().random
            __headers = {"user-agent": __user}

            
            _url = f"https://rur.hitmotop.com/search?q={self.music_name}"
            _response = requests.get(_url, headers=__headers)
            _soup = BeautifulSoup(_response.text, "lxml")
            try:
                if _soup.find('h2',class_='tracks__title content-item-title').text:
                    raise NoFoundTrack
            except AttributeError:
                pass



            # получаем информацию о треках
            _track_titles = [i.text.strip() for i in _soup.find_all("div", class_="track__title")]
            _track_artists = [i.text.strip() for i in _soup.find_all("div", class_="track__desc")]
            _track_duration = [i.text.strip() for i in _soup.find_all("div", class_="track__fulltime")]
            _track_pictures = [f"{i.get('style')[23:-3]}" for i in _soup.find_all("div", class_="track__img")]
            _track_urls_dow = [i.get('href') for i in _soup.find_all('a', class_='track__download-btn')]
            _track_url = [f"https://rur.hitmotop.com{tra_url.get('href')}" for tra_url in _soup.find_all('a', class_='track__info-l')]

            _items = []
            for idx in range(min(len(_track_titles), self.amount)):
                if self.get_redirect_url and len(_track_urls_dow[idx])>0:
                    direct_download_link = requests.get(_track_urls_dow[idx],headers=__headers,allow_redirects=True).url
                    print(f'Получил прямую ссылку: {direct_download_link}')
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

            self.count_tracks = len(_items)
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
    