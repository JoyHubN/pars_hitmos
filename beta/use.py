from async_down import main
from sync_p.rating_tracks_count import RatingTracks
import time,os, asyncio


os.system('cls')

start_time_all = time.time()

start_time1 = time.time()
mus = RatingTracks.get_tracks(10)
print(f'\n1 ЗАПРОС ЗА {time.time() - start_time1}\n\n')

# start_time2 = time.time()
# mus1 = entered_tracks.Entered_Track_48.get('linkin park',10)
# print(f'\n2 ЗАПРОС ЗА {time.time() - start_time2}\n\n')

start_time_d1 = time.time()
asyncio.run(main(mus))
print(f'\n1 СКАЧАН ЗА {time.time() - start_time_d1}\n\n')

# start_time_d2 = time.time()
# asyncio.run(main(mus1))
# print(f'\n\n2 СКАЧАН ЗА {time.time() - start_time_d2}\n\n')
print(f'\nВСЕГО ЗА {time.time() - start_time_all}\n\n')