from bs4 import BeautifulSoup

from parse_hitmos.tools.headers import get_headers
from parse_hitmos.excepts import CountTracksErr, RedirectErr
from parse_hitmos.tools.base_session import BaseSessionHandlerRating
from parse_hitmos.tools.retry_func import safe_get, safe_head
from parse_hitmos.tools.replace_symbol import replace_symbol_in_title


class RatingCount(BaseSessionHandlerRating):
    '''
    Класс для получения списка рейтинговых треков.\n
    :param count: число от 1 до 48 - количество треков\n
    :param get_redirect_url: True-получить прямую ссылку на скачивание трека\n
    :type count: int\n
    :type get_redirect_url: bool

    .. note:: Установка get_redirect_url=True может значительно увеличить время выполнения.\n
    Методы:\n
        - get_author -> list[str]: автор трека
        - get_title -> list[str]: название трека
        - get_url_down -> list[str]: ссылка на скачивание трека
        - direct_download_link -> list[str]: прямая ссылка на скачивание трека
        - get_duration -> list[str]: длительность трека
        - get_picture_url -> list[str]: ссылка на обложку трека
        - get_url_track -> list[str]: ссылка на трек
    '''

    def __init__(self, count_tracks, get_redirect_url=False):
        if not isinstance(count_tracks, int): raise CountTracksErr
        if not isinstance(get_redirect_url, bool): raise RedirectErr

        self.count_tracks = count_tracks
        self.get_redirect_url = get_redirect_url

        super().__init__()
        
        self.count_selection
    
    @property
    def count_selection(self) -> dict[str, list[dict[str, None | str]]]:
        
        if self.count_tracks > 48: 
            raise ValueError('Only <= 48')
        
        else:
            __headers = get_headers()
            request = safe_get(self, self.song_rated, headers=__headers)
            _soup = BeautifulSoup(request.text, 'html.parser')

            _track_titles = [i.text.strip() for i in _soup.find_all("div", class_="track__title")]
            _track_artists = [i.text.strip() for i in _soup.find_all("div", class_="track__desc")]
            _track_duration = [i.text.strip() for i in _soup.find_all("div", class_="track__fulltime")]
            _track_pictures = [f"{i.get('style')[23:-3]}" for i in _soup.find_all("div", class_="track__img")]
            _track_urls_dow = [i.get('href') for i in _soup.find_all('a', class_='track__download-btn')]
            _track_url = [f"{self.base_url[:-1]}{tra_url.get('href')}" for tra_url in _soup.find_all('a', class_='track__info-l')]

            _items = []

            for idx in range(self.count_tracks if len(_track_titles) > self.count_tracks else len(_track_titles)):
                if self.get_redirect_url and len(_track_urls_dow[idx]) > 0:
                    direct_download_link = safe_head(self, _track_urls_dow[idx], headers=__headers, allow_redirects=True, timeout=5).url   
                else: direct_download_link = None
                item = {
                    'author': _track_artists[idx],
                    'title': replace_symbol_in_title(_track_titles[idx]),
                    'url_down': _track_urls_dow[idx],
                    'direct_download_link': direct_download_link,
                    'duration_track': _track_duration[idx],
                    'picture_url': _track_pictures[idx],
                    'url_track': _track_url[idx]
                }
                _items.append(item)

            self.session.close()
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
    def direct_download_link(self) -> list[None | str]:
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
    def get_all(self): return self.data
    
    @property
    def get_author_title(self) -> list[str]:
        __author = self.get_author
        __title = self.get_title
        return [f'{__author[i]} - {__title[i]}' for i in range(self.count_tracks)]