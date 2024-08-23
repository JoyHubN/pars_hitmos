import fake_useragent, requests
from bs4 import BeautifulSoup
from .excepts import NoFoundTrack, MaxTrack, MusicName, AmountErr, RedirectErr

class EnteredTrack:
    """
Треки из запроса\n
:param music_name: Название и автор трека в одной строке. - str
:param amount: Количество треков, которое нужно вывести. Max 48. - int
:param get_redirect_url: bool тип, True-получить прямую ссылку на скачивание трека, но увеличивает время выполнения\n
Для получения информации доступны след.функции:
    - get_author: list, автор трека;
    - get_title: list, название трека;
    - get_url_down: list, ссылка на скачивание трека;
    - direct_download_link: list прямая ссылка на скачивание трека;
    - get_duration: list, длительность трека;
    - get_picture_url: list, ссылка на обложку трека;
    - get_url_track: list, ссылка на трек.
 
    """


    def __init__(self, music_name:str, amount: int, get_redirect_url=False):
        if isinstance(music_name, str) is False: raise MusicName
        if isinstance(amount, int) is False: raise AmountErr
        if isinstance(get_redirect_url, bool) is False: raise RedirectErr

        self.music_name = music_name
        self.amount = int(amount)
        self.get_redirect_url = get_redirect_url
        self.get_info
        

    @property
    def get_info(self):

        if self.amount > 48:
            raise MaxTrack
        else:
            __user = fake_useragent.UserAgent().random
            __headers = {"user-agent": __user}
            __url11= requests.get('https://hitmos.me/', headers=__headers, allow_redirects=True).url
            __url1= __url11[:-1] if '/' in __url11[:-1] else __url11
            
            _url = f"{__url1}{'/' if '/' in __url1[:-1] else ''}search?q={self.music_name}"

            _response = requests.get(_url, headers=__headers)
            _soup = BeautifulSoup(_response.text, "html.parser")

            
            if _soup.find('h2',class_='tracks__title content-item-title'):
                raise NoFoundTrack



            # получаем информацию о треках
            _track_titles = [i.text.strip() for i in _soup.find_all("div", class_="track__title")]
            _track_artists = [i.text.strip() for i in _soup.find_all("div", class_="track__desc")]
            _track_duration = [i.text.strip() for i in _soup.find_all("div", class_="track__fulltime")]
            _track_pictures = [f"{i.get('style')[23:-3]}" for i in _soup.find_all("div", class_="track__img")]
            _track_urls_dow = [i.get('href') for i in _soup.find_all('a', class_='track__download-btn')]
            _track_url = [f"{__url1}{tra_url.get('href')}" for tra_url in _soup.find_all('a', class_='track__info-l')]

            _items = []
            for idx in range(len(_track_titles)):
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

            self.count_tracks = len(_items)
            self.data = {"items": _items}
            return self.data
    
    @property
    def get_author(self) -> list[str]:
        return [item['author'] for item in self.data['items']]    
    
    @property
    def get_title(self) -> list[str]:
        return [item['title'] for item in self.data['items']]
    
    @property
    def get_url_down(self) -> list[str]:
        return [item['url_down'] for item in self.data['items']]

    @property
    def direct_download_link(self) -> list[str]:
        return [item['direct_download_link'] for item in self.data['items']]

    @property
    def get_duration(self) -> list[str]:
        return [item['duration_track'] for item in self.data['items']]
    
    @property
    def get_picture_url(self) -> list[str]:
        return [item['picture_url'] for item in self.data['items']]
    
    @property
    def get_url_track(self) -> list[str]:
        return [item['url_track'] for item in self.data['items']]
    
    @property
    def get_author_title(self) -> list[str]:
        __author = self.get_author
        __title = self.get_title
        return [f'{__author[i]} - {__title[i]}' for i in range(self.count_tracks)]
            
            
            
    