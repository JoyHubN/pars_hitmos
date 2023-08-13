import tqdm, time, os, textwrap, requests
# from pars_hitmotop import entered_tracks
# from async_p.rating_tracks import RatingTracksPage
# from sync_p.entered_tracks import Entered_Track_48
from sync_p.entered_tracks import Entered_Track_48





def down_mus(url: str, filname: str):
    with open(f'C:/Users/User/Desktop/tg_bot_mus/post_tg/1/pars_hitmotop/beta/mus/{filname}.mp3', 'wb') as f:
        with requests.get(url, stream=True) as r:
          
            total = int(r.headers.get('content-length', 0))
            tqdm_items = {
                'total': total,
                'miniters': 1,
                'unit_scale': True,
                'unit_divisor': 1024,
                'colour': 'green',
                'bar_format': "{desc} {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}"
            }

            with tqdm.tqdm(**tqdm_items) as pb:
                shortened_title = textwrap.shorten(filname, width=20, placeholder='...')
                pb.set_description(shortened_title)  # Установка описания без "it"
                for chunk in r.iter_content(chunk_size=8192):
                    pb.update(len(chunk))
                    f.write(chunk)
def main(data):
    tasks = [(down_mus(i['url_down'], 
    f"{i['author']} - {i['title']}")) for i in data['response']['items']]
   
        


os.system('cls')

start_time_all = time.time()





start_time1 = time.time()
mus = Entered_Track_48.get('alan walker',10)
print(f'\n1 ЗАПРОС ЗА {time.time() - start_time1}\n\n')

# start_time2 = time.time()
# mus1 = entered_tracks.Entered_Track_48.get('linkin park',10)
# print(f'\n2 ЗАПРОС ЗА {time.time() - start_time2}\n\n')

start_time_d1 = time.time()
main(mus)
print(f'\n1 СКАЧАН ЗА {time.time() - start_time_d1}\n\n')

# start_time_d2 = time.time()
# asyncio.run(main(mus1))
# print(f'\n\n2 СКАЧАН ЗА {time.time() - start_time_d2}\n\n')
print(f'\nВСЕГО ЗА {time.time() - start_time_all}\n\n')
