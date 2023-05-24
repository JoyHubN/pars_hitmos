'''Рейтинговые треки'''
class rating_tr_count:
    def count_selection(count):
        '''
    Функция для получения списка треков с сайта ru.hitmotop.com.
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
        if count >48: 
            raise ValueError('Only <= 48')
        else:
            import fake_useragent, requests
            from bs4 import BeautifulSoup
            __user = fake_useragent.UserAgent().random
            __headers = {'user-agent': __user}
 
            __list = []
            url = 'https://ru.hitmotop.com/songs/top-rated'
            response = requests.get(url, headers=__headers)
            soup = BeautifulSoup(response.text, 'lxml')
            naz_track = soup.find_all('div', class_='track__title')
            musikant_track = soup.find_all('div', class_='track__desc')
            duration_track = soup.find_all('div', class_='track__fulltime')
            picture_url = soup.find_all('div', class_='track__img')
            url_track = soup.find_all('a', class_="track__info-l")
            track_dow_url = soup.find_all('a', class_='track__download-btn')

            fg = 0
            for i, track in enumerate(naz_track):
                if fg != count:
                    __list.append({
                        'author': musikant_track[i].text,
                        'title': track.text.lstrip().lstrip().lstrip().lstrip().rstrip(),
                        'url_track': f'https://ru.hitmotop.com{url_track[i].get("href").lstrip()}',
                        'url_down': f"{track_dow_url[i].get('href')}",
                        'duration_track': duration_track[i].text,
                        'picture_url': f'https://ru.hitmotop.com{picture_url[i].get("style")[23:-3]}'
                    })
                    fg+=1

            return {'response': {'items': __list}}
                
            

