import fake_useragent
import httpx
import asyncio
from bs4 import BeautifulSoup


class RatingTrackCount:
    @staticmethod
    async def async_get_item_info(url, headers, semaphore):
        async with semaphore:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                return response.text

    @staticmethod
    async def async_get(count):
        if count > 48:
            raise ValueError('Only <= 48')
        else:
            __user = fake_useragent.UserAgent().random
            __headers = {'user-agent': __user}

            __list = []
            url = 'https://rur.hitmotop.com/songs/top-rated'
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=__headers)
                soup = BeautifulSoup(response.text, 'lxml')

            naz_track = soup.find_all('div', class_='track__title')
            musikant_track = soup.find_all('div', class_='track__desc')
            duration_track = soup.find_all('div', class_='track__fulltime')
            picture_url = soup.find_all('div', class_='track__img')
            url_track = soup.find_all('a', class_="track__info-l")
            track_dow_url = soup.find_all('a', class_='track__download-btn')

            __list = []
            for i, (track, musikant, duration, pic, url, down_url) in enumerate(
                zip(naz_track, musikant_track, duration_track, picture_url, url_track, track_dow_url)
            ):
                if i >= count:
                    break

                __list.append({
                    'author': musikant.text,
                    'title': track.text.strip(),
                    'url_track': f'https://rur.hitmotop.com{url.get("href").lstrip()}',
                    'url_down': f"{down_url.get('href')}",
                    'duration_track': duration.text,
                    'picture_url': f'https://rur.hitmotop.com{pic.get("style")[23:-3]}'
                })

            return {'response': {'items': __list}}

    @staticmethod
    def get(count):
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
        return asyncio.run(RatingTrackCount.async_get(count))
