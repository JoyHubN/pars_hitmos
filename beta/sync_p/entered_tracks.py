import fake_useragent
import requests
from bs4 import BeautifulSoup
from itertools import islice

class Entered_Track_48:
    def __init__(self, music_name: str, amount: int):
        self.music_name = music_name
        self.amount = amount

    @staticmethod
    def get(music_name: str, amount: int):
        if amount > 48:
            raise ValueError("The number of tracks should not exceed 48")
        else:
            __user = fake_useragent.UserAgent().random
            __headers = {"user-agent": __user}
            __list = []

            url = f"https://rur.hitmotop.com/search?q={music_name}"
            response = requests.get(url, headers=__headers)
            soup = BeautifulSoup(response.text, "lxml")
            try:
                if soup.find('h2', class_='tracks__title content-item-title').text:
                    raise ValueError('Nothing was found for your query')
            except AttributeError:
                pass

            track_titles = [i.text.strip() for i in soup.find_all("div", class_="track__title")]
            track_artists = [i.text.strip() for i in soup.find_all("div", class_="track__desc")]
            track_duration = [i.text.strip() for i in soup.find_all("div", class_="track__fulltime")]
            track_pictures = [f"https://rur.hitmotop.com{i.get('style')[23:-3]}" for i in soup.find_all("div", class_="track__img")]
            track_urls_dow = [i.get('href') for i in soup.find_all('a', class_='track__download-btn')]
            track_url = [f"https://rur.hitmotop.com{tra_url.get('href')}" for tra_url in soup.find_all('a', class_='track__info-l')]

            items = []
            for track_artist, track_title, track_url_dow, track_dur, track_pic, track_ur in islice(zip(track_artists, track_titles, track_urls_dow, track_duration, track_pictures, track_url), amount):
                item = {
                    'author': track_artist,
                    'title': track_title,
                    'url_down': track_url_dow,
                    'duration_track': track_dur,
                    'picture_url': track_pic,
                    'url_track': track_ur
                }
                items.append(item)

            return {"response": {"items": items}}
