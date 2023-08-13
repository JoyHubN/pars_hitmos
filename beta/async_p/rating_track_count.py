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

            fg = 0
            semaphore = asyncio.Semaphore(10)  # Control concurrent async tasks
            tasks = []
            for i, track_url in enumerate(url_track):
                task = asyncio.create_task(
                    RatingTrackCount.async_get_item_info(f'https://rur.hitmotop.com{track_url.get("href").lstrip()}', __headers, semaphore)
                )
                tasks.append(task)

            responses = await asyncio.gather(*tasks)

            for i, track in enumerate(naz_track):
                if fg != count:
                    __list.append({
                        'author': musikant_track[i].text,
                        'title': track.text.lstrip().lstrip().lstrip().lstrip().rstrip(),
                        'url_track': f'https://rur.hitmotop.com{url_track[i].get("href").lstrip()}',
                        'url_down': f"{track_dow_url[i].get('href')}",
                        'duration_track': duration_track[i].text,
                        'picture_url': f'https://rur.hitmotop.com{picture_url[i].get("style")[23:-3]}'
                    })
                    fg += 1

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


