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
    async def async_get(page_number):
        if page_number > 11:
            raise ValueError('Only <= 11')
        else:
            __user = fake_useragent.UserAgent().random
            __headers = {'user-agent': __user}
            if page_number == 1:
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

                for i, track in enumerate(naz_track):
                    __list.append({
                        'author': musikant_track[i].text,
                        'title': track.text.lstrip().lstrip().lstrip().lstrip().rstrip(),
                        'url_track': f'https://rur.hitmotop.com{url_track[i].get("href").lstrip()}',
                        'url_down': f"{track_dow_url[i].get('href')}",
                        'duration_track': duration_track[i].text,
                        'picture_url': f'https://rur.hitmotop.com{picture_url[i].get("style")[23:-3]}'
                    })
                return {'response': {'items': __list}}

            else:
                page_number *= 48
                __list = []

                url = 'https://rur.hitmotop.com/songs/top-rated/start/'

                semaphore = asyncio.Semaphore(10)  # Control concurrent async tasks
                tasks = []
                for cf in range(0, page_number, 48):
                    task = asyncio.create_task(
                        RatingTracksPage.async_get_item_info(f'{url}{cf}', __headers, semaphore)
                    )
                    tasks.append(task)

                responses = await asyncio.gather(*tasks)

                for response in responses:
                    soup = BeautifulSoup(response, 'lxml')

                    track_titles = [i.text.strip() for i in soup.find_all("div", class_="track__title")]
                    track_artists = [i.text.strip() for i in soup.find_all("div", class_="track__desc")]
                    track_duration = [i.text.strip() for i in soup.find_all("div", class_="track__fulltime")]
                    track_pictures = [f"https://rur.hitmotop.com{i.get('style')[23:-3]}" for i in soup.find_all("div", class_="track__img")]
                    track_urls_dow = [f"{track_dow_url.get('href')}" for track_dow_url in soup.find_all('a', class_='track__download-btn')]
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
