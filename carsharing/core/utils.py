import asyncio
import aiohttp
from collections import deque
from time import time
from django.conf import settings

# ======================================================================
# fixture sample image download fns


def write_image(data, path):
    name = 'file-{}.jpeg'.format(int(time()*1000))
    filename = f'{path}/{name}'
    with open(filename, 'wb') as file:
        file.write(data)
    # print(f'saved:{filename}')
    return name


async def fetch_content(url, session: aiohttp.ClientSession, save_path, category):
    async with session.get(url, allow_redirects=True) as responce:
        data = await responce.read()
        fn = write_image(data, path=save_path)
        files.append(f'./{category}/{fn}')


async def create_job(n, theme, resol, category):

    url = f'https://loremflickr.com/{resol[0]}/{resol[1]}/{theme}'

    q = deque()
    static_prefix = settings.MEDIA_ROOT
    save_path = f'{static_prefix}/{category}'

    async with aiohttp.ClientSession() as session:
        for i in range(n):
            q.append(asyncio.create_task(fetch_content(url, session, save_path, category)))
        await asyncio.gather(*q)

files = []

def get_n_photo_by_theme(n, theme, resol, category):
    global files
    files = []
    asyncio.run(create_job(n, theme, resol, category))
    return files


# ======================================================================

lang_acronyms = {}
