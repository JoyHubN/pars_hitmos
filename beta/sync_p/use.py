import os, time
from sync_down import down_mus
from entered_tracks import Entered_Track_48
os.system('cls')

def main(data):
    tasks = [(down_mus(i['url_down'], 
    f"{i['author']} - {i['title']}")) for i in data['response']['items']]
   


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

