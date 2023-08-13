import asyncio
import httpx
import tqdm, time, os, textwrap
# from pars_hitmotop import entered_tracks
# from rating_tracks import RatingTracksPage
# from entered_tracks import Entered_Track_48
# from rating_tracks_count import rating_tr_count






async def down_mus(url: str, filname: str, semaphore: asyncio.Semaphore):
    async with semaphore:
        with open(f'C:/Users/User/Desktop/tg_bot_mus/post_tg/1/pars_hitmotop/beta/mus/{filname}.mp3', 'wb') as f:
            async with httpx.AsyncClient() as client:
                async with client.stream('GET', url, follow_redirects=False) as r:
                    redir = r.headers.get('location')
                    if redir:
                        async with client.stream('GET', redir) as red_res:
                            red_res.raise_for_status()
                            total = int(red_res.headers.get('content-length', 0))
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
                                async for chunk in red_res.aiter_bytes():
                                    pb.update(len(chunk))
                                    f.write(chunk)
                    else:
                        r.raise_for_status()

async def main(data):
    concurrency = 2  # Количество одновременных загрузок
    semaphore = asyncio.Semaphore(concurrency)
    loop = asyncio.get_running_loop()

    tasks = [loop.create_task(down_mus(i['url_down'], 
    f"{i['author']} - {i['title']}", semaphore)) for i in
             data['response']['items']]

    await asyncio.gather(*tasks, return_exceptions=True)


