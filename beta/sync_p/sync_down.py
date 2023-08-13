import tqdm, time, os, textwrap, requests

# from rating_tracks import RatingTracksPage






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

