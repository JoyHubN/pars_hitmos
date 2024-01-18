import asyncio
import httpx
import tqdm
import fake_useragent
from bs4 import BeautifulSoup

class Entered_Track_48:
    def __init__(self, music_name: str, amount: int):
        self.music_name = music_name
        self.amount = amount

    @staticmethod
    async def async_get_item_info(url, headers, semaphore):
        async with semaphore:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                return response.text

    @staticmethod
    async def async_get(music_name: str, amount: int):
        if amount > 48:
            raise ValueError("The number of tracks should not exceed 48")

        __user = fake_useragent.UserAgent().random
        __headers = {"user-agent": __user}
        __list = []
        for _ in range(amount):
            __list.append({"author": "", "title": "", "url_down": "", "duration_track": "", "picture_url": "", "url_track": ""})

        url = f"https://rur.hitmotop.com/search?q={music_name}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=__headers)
            soup = BeautifulSoup(response.text, "lxml")

            track_titles = [i.text.strip() for i in soup.find_all("div", class_="track__title")]
            track_artists = [i.text.strip() for i in soup.find_all("div", class_="track__desc")]
            track_duration = [i.text.strip() for i in soup.find_all("div", class_="track__fulltime")]
            track_pictures = [f"https://rur.hitmotop.com{i.get('style')[23:-3]}" for i in soup.find_all("div", class_="track__img")]
            track_urls_dow = [i.get('href') for i in soup.find_all('a', class_='track__download-btn')]
            track_url = [f"https://rur.hitmotop.com{tra_url.get('href')}" for tra_url in soup.find_all('a', class_='track__info-l')]

            items = []
            semaphore = asyncio.Semaphore(10)  # Control concurrent async tasks
            tasks = []
            for idx, track_url in enumerate(track_url):
                task = asyncio.create_task(
                    Entered_Track_48.async_get_item_info(track_url, __headers, semaphore)
                )
                tasks.append(task)

            responses = await asyncio.gather(*tasks)

            for idx, track in enumerate(__list):
                try:
                    item = {}
                    # ... (parse responses[idx] here)
                    item['author'] = track_artists[idx]
                    item['title'] = track_titles[idx]
                    item['url_down'] = track_urls_dow[idx]
                    item['duration_track'] = track_duration[idx]
                    item['picture_url'] = track_pictures[idx]
                    item['url_track'] = track_url[idx]
                    items.append(item)
                except:
                    pass

            return {"response": {"items": items}}

    @staticmethod
    def get(music_name: str, amount: int):
        return asyncio.run(Entered_Track_48.async_get(music_name, amount))


