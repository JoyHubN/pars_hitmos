'''Треки из переданного запроса'''

class Entered_Track_48():
    def __init__(self, music_name:str, amount:int):
        self.music_name = music_name
        self.amount = amount
    @staticmethod
    def get(music_name=str, amount=int):
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
        if amount > 48:
            raise ValueError("The number of tracks should not exceed 48")
        else:
            import fake_useragent, requests
            from bs4 import BeautifulSoup
            __user = fake_useragent.UserAgent().random
            __headers = {"user-agent": __user}
            __list = []
            for _ in range(amount):
                __list.append({"author": "", "title": "", "url_down": "", "duration_track": "", "picture_url": "", "url_track": ""})

            url = f"https://rur.hitmotop.com/search?q={music_name}"
            response = requests.get(url, headers=__headers)
            soup = BeautifulSoup(response.text, "lxml")
            try:
                if soup.find('h2',class_='tracks__title content-item-title').text:
                    raise ValueError('Nothing was found for your query')
            except AttributeError:
                pass



            # получаем информацию о треках
            track_titles = [i.text.strip() for i in soup.find_all("div", class_="track__title")]
            track_artists = [i.text.strip() for i in soup.find_all("div", class_="track__desc")]
            track_duration = [i.text.strip() for i in soup.find_all("div", class_="track__fulltime")]
            track_pictures = [f"https://rur.hitmotop.com{i.get('style')[23:-3]}" for i in soup.find_all("div", class_="track__img")]
            track_urls_dow = [i.get('href') for i in soup.find_all('a', class_='track__download-btn')]
            track_url = [f"https://rur.hitmotop.com{tra_url.get('href')}" for tra_url in soup.find_all('a', class_='track__info-l')]

            items = []
            for idx, track in enumerate(__list):
                try:
                    item = {}
                    item['author'] = track_artists[idx]
                    item['title'] = track_titles[idx]
                    item['url_down'] = track_urls_dow[idx]
                    item['duration_track'] = track_duration[idx]
                    item['picture_url'] = track_pictures[idx]
                    item['url_track'] = track_url[idx]
                    items.append(item)
                except:
                    pass

            return {"response":{"items": items}}