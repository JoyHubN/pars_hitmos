from bs4 import BeautifulSoup
from urllib.parse import urljoin

from parse_hitmos.tools.headers import get_headers
from parse_hitmos.excepts import PageError, RedirectErr, PageCount
from parse_hitmos.tools.base_session import BaseSessionHandlerRatingPage
from parse_hitmos.tools.retry_func import safe_get, safe_head
from parse_hitmos.tools.replace_symbol import replace_symbol_in_title


class RatingPage(BaseSessionHandlerRatingPage):
    '''
    Функция для получения списка рейтинговых треков\n
    :param page_count: число от 1 до 11 (номер страницы с треками)
    :param get_redirect_url: True-получить прямую ссылку на скачивание трека, но увеличивает время выполнения
    :type page_count: int
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
    def __init__(self, page_count:int, get_redirect_url=False):
        if not isinstance(page_count, int): raise PageCount
        if not isinstance(get_redirect_url, bool): raise RedirectErr
        
        self.page_count = int(page_count)
        self.get_redirect_url = get_redirect_url

        super().__init__()

        self.__page_selection


    @property
    def __page_selection(self):
 
        if self.page_count > 11: 
            raise PageError
        else:
            
            
            if self.page_count == 1:
                __list = []
                __headers = get_headers()
                response = safe_get(self, self.song_rated, headers=__headers, timeout=10, allow_redirects=self.get_redirect_url)
                _soup = BeautifulSoup(response.text, 'html.parser')
                if not self.get_redirect_url: self.session.close()

                
                _track_titles = [i.text.strip() for i in _soup.find_all("div", class_="track__title")]
                _track_artists = [i.text.strip() for i in _soup.find_all("div", class_="track__desc")]
                _track_duration = [i.text.strip() for i in _soup.find_all("div", class_="track__fulltime")]
                _track_pictures = [f"{i.get('style')[23:-3]}" for i in _soup.find_all("div", class_="track__img")]
                _track_urls_dow = [i.get('href') for i in _soup.find_all('a', class_='track__download-btn')]
                _track_url = [f"{self.base_url[:-1]}{tra_url.get('href')}" for tra_url in _soup.find_all('a', class_='track__info-l')]
                
                for idx in range(0, len(_track_titles)):
                    if self.get_redirect_url and len(_track_urls_dow[idx]) > 0:
                        try:
                            direct_download_link = self.session.head(_track_urls_dow[idx], headers=__headers, allow_redirects=True).url
                        except Exception as err:
                            print(err)

                            direct_download_link = safe_head(self, _track_urls_dow[idx], headers=__headers, allow_redirects=True)
                            direct_download_link = direct_download_link.url
                    else: 
                        direct_download_link = None
                    
                    items={
                        'author': _track_artists[idx],
                        'title':  replace_symbol_in_title(_track_titles[idx]),
                        'url_down': _track_urls_dow[idx],
                        'direct_download_link': direct_download_link,
                        'url_track': _track_url[idx],
                        'duration_track': _track_duration[idx],
                        'picture_url': _track_pictures[idx]
                    }
                    __list.append(items)
                
                self.count_tracks = len(__list)
                self.data = {'items': __list}
                return self.data
                
            else: 
                self.page_count *= 48

                __list = []

                items = []
                for page in range(0, self.page_count, 48):
                    __headers = get_headers()
                    response = safe_get(self, urljoin(self.song_rated_more1, str(page)), cookies={'sid':self.sid.get_sid()}, headers=__headers, timeout=5)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    if not self.get_redirect_url: self.session.close()

                    track_titles = [i.text.strip() for i in soup.find_all("div", class_="track__title")]
                    track_artists = [i.text.strip() for i in soup.find_all("div", class_="track__desc")]
                    track_duration = [i.text.strip() for i in soup.find_all("div", class_="track__fulltime")]
                    track_pictures = [f"{i.get('style')[23:-3]}" for i in soup.find_all("div", class_="track__img")]
                    track_urls_dow = [f"{track_dow_url.get('href')}" for track_dow_url in soup.find_all('a', class_='track__download-btn')]
                    track_url = [f"{self.base_url[:-1]}{tra_url.get('href')}" for tra_url in soup.find_all('a', class_='track__info-l')]

                    for idx in range(0, len(track_titles)):
                        if self.get_redirect_url and len(track_urls_dow[idx]) > 0:
                            try:
                                direct_download_link = self.session.head(track_urls_dow[idx], headers=__headers, allow_redirects=True).url
                            except Exception as err:
                                print(err)                              
                            
                                direct_download_link = safe_get(self, track_urls_dow[idx], headers=__headers, allow_redirects=True)
                                direct_download_link = direct_download_link.url

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
                self.session.close()
                self.count_tracks = len(__list)
                self.data = {'items': __list}
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
    def direct_download_link(self)  -> list[None | str]:
        return [item['direct_download_link'] for item in self.data['items']]

    @property
    def get_duration(self)  -> list[str]:
        return [item['duration_track'] for item in self.data['items']]
    
    @property
    def get_picture_url(self)  -> list[str]:
        return [item['picture_url'] for item in self.data['items']]
    
    @property
    def get_url_track(self)  -> list[str]:
        return [item['url_track'] for item in self.data['items']]

    @property
    def get_all(self)  -> list[str]: return self.data
        
    @property
    def get_author_title(self) -> list[str]:
        __author = self.get_author
        __title = self.get_title
        return [f'{__author[i]} - {__title[i]}' for i in range(self.count_tracks)]