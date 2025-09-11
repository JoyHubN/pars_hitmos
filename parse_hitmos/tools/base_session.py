import requests
from urllib.parse import urljoin
from requests.exceptions import ReadTimeout

from parse_hitmos.excepts import MaxAttempts
from parse_hitmos.config.load_data import SID
from parse_hitmos.tools.headers import get_headers
from parse_hitmos.tools.retry_func import safe_get_main_url

class BaseSessionHandlerRating:
    def __init__(self):
        self.__attempt = 0
        self.max_attempt = 10
        self.session = None
        self.sid = SID()
        self.base_url = ''
        self.song_rated = ''
        self.create_session()

    def create_session(self):
        
        __headers = get_headers()
        cookies = {'sid': self.sid.get_sid()}        
        
        self.session = requests.Session()
        response = safe_get_main_url(self, 'https://hitmos.me', headers=__headers, cookies=cookies, timeout=5)
        
        if response.status_code == 403:
            response = self.session.get('https://hitmos.me/', cookies={'sid':self.sid.get_sid()}, headers=__headers, allow_redirects=True)
            self.sid.write_sid(self.session.cookies.get_dict())

        self.base_url = response.url
        self.song_rated = urljoin(response.url, 'songs/top-rated')



class BaseSessionHandlerRatingPage:
    def __init__(self):
        self.__attempt = 0
        self.max_attempt = 10
        self.session = None
        self.sid = SID()
        self.base_url = ''
        self.song_rated = ''
        self.create_session()

    def create_session(self):
        
        __headers = get_headers()
        cookies = {'sid': self.sid.get_sid()}        
    
        self.session = requests.Session()
        response = safe_get_main_url(self, 'https://hitmos.me', headers=__headers, cookies=cookies, timeout=5)

        
        self.base_url = response.url
        self.song_rated_more1 = urljoin(response.url, 'songs/top-rated/start/')
        self.song_rated = urljoin(response.url, 'songs/top-rated')


class BaseSessionHandlerInputTracks:
    def __init__(self):
        self.__attempt = 0
        self.max_attempt = 10
        self.base_url = None
        self.search_url = None
        self.session = None
        self.sid = SID()
        self.create_session()

    def create_session(self):
        __headers = get_headers()
        cookies = {'sid': self.sid.get_sid()}        
    
        while self.__attempt < self.max_attempt:
            try:
                self.session = requests.Session()
                if len(cookies['sid']) == 0:
                    response = self.session.get('https://hitmos.me/', headers=__headers, allow_redirects=True, timeout=(5, 15))    
                else:
                    self.session.cookies.update(cookies)
                    response = self.session.get('https://hitmos.me/', headers=__headers, allow_redirects=True, timeout=(5, 15))
                
                if response.status_code == 200:
                    response = self.session.get(response.url, headers=__headers)
                    if len(self.session.cookies.get_dict()) == 0:
                        continue
                    else:
                        self.sid.write_sid(self.session.cookies.get_dict())
                        break
                else:
                    response = self.session.get('https://hitmos.me/', headers=__headers, allow_redirects=True, timeout=5)
                    if response.status_code == 200:
                        self.sid.write_sid(self.session.cookies.get_dict())
                        break
            except ReadTimeout as err:
                self.__attempt +=1
                cookies = {}
                print(err)
                self.session.cookies.clear()
                cookies = {}
                self.session.close()
            else:
                self.__attempt = 0
                print('Произошла непредвиденная ситуация', __file__)
                
        else:
            raise MaxAttempts(self.max_attempt)
        
        self.base_url = response.url
        self.search_url = urljoin(self.base_url, 'search?q=')