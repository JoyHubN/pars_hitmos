import fake_useragent
import httpx
import asyncio
from bs4 import BeautifulSoup

class RatingTracksPage:
    @staticmethod
    async def async_get_item_info(url, headers, semaphore):
        async with semaphore:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                return response.text

    @staticmethod
    async def async_get_page(page_url, __headers, semaphore):
        async with semaphore:
            async with httpx.AsyncClient() as client:
                response = await client.get(page_url, headers=__headers)
                return response.text

    @staticmethod
    async def async_get(page_number):
        if page_number > 11:
            raise ValueError('Only <= 11')

        __user = fake_useragent.UserAgent().random
        __headers = {'user-agent': __user}

        if page_number == 1:
            url = 'https://rur.hitmotop.com/songs/top-rated'
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=__headers)
                soup = BeautifulSoup(response.text, 'lxml')

            track_titles = [i.text.strip() for i in soup.find_all("div", class_="track__title")]
            track_artists = [i.text.strip() for i in soup.find_all("div", class_="track__desc")]
            track_duration = [i.text.strip() for i in soup.find_all("div", class_="track__fulltime")]
            track_pictures = [f"https://rur.hitmotop.com{i.get('style')[23:-3]}" for i in soup.find_all("div", class_="track__img")]
            track_urls_dow = [f"{track_dow_url.get('href')}" for track_dow_url in soup.find_all('a', class_='track__download-btn')]
            track_url = [f"https://rur.hitmotop.com{tra_url.get('href')}" for tra_url in soup.find_all('a', class_='track__info-l')]

            items = []
            for track in zip(track_artists, track_titles, track_urls_dow, track_duration, track_pictures, track_url):
                item = {
                    'author': track[0],
                    'title': track[1],
                    'url_down': track[2],
                    'duration_track': track[3],
                    'picture_url': track[4],
                    'url_track': track[5]
                }
                items.append(item)

            return {'response': {'items': items}}

        else:
            page_number *= 48
            url = 'https://rur.hitmotop.com/songs/top-rated/start/'

            semaphore = asyncio.Semaphore(10)  # Control concurrent async tasks
            tasks = []
            for cf in range(0, page_number, 48):
                page_url = f'{url}{cf}'
                task = asyncio.create_task(
                    RatingTracksPage.async_get_page(page_url, __headers, semaphore)
                )
                tasks.append(task)

            responses = await asyncio.gather(*tasks)

            items = []
            for response in responses:
                soup = BeautifulSoup(response, 'lxml')
                track_titles = [i.text.strip() for i in soup.find_all("div", class_="track__title")]
                track_artists = [i.text.strip() for i in soup.find_all("div", class_="track__desc")]
                track_duration = [i.text.strip() for i in soup.find_all("div", class_="track__fulltime")]
                track_pictures = [f"https://rur.hitmotop.com{i.get('style')[23:-3]}" for i in soup.find_all("div", class_="track__img")]
                track_urls_dow = [f"{track_dow_url.get('href')}" for track_dow_url in soup.find_all('a', class_='track__download-btn')]
                track_url = [f"https://rur.hitmotop.com{tra_url.get('href')}" for tra_url in soup.find_all('a', class_='track__info-l')]

                parsed_items = []
                for track in zip(track_artists, track_titles, track_urls_dow, track_duration, track_pictures, track_url):
                    item = {
                        'author': track[0],
                        'title': track[1],
                        'url_down': track[2],
                        'duration_track': track[3],
                        'picture_url': track[4],
                        'url_track': track[5]
                    }
                    parsed_items.append(item)

                items.extend(parsed_items)

            return {"response": {"items": items}}

    @staticmethod
    def get(page_number):
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
        return asyncio.run(RatingTracksPage.async_get(page_number))
