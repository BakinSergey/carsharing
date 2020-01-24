import asyncio
import aiohttp
from collections import deque
from time import time
from django.conf import settings


# ======================================================================
# fixture sample image download fns


def write_image(data, path):
    name = 'file-{}.jpeg'.format(int(time() * 1000))
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

# ======================================================================

color_map = {

    'red': {'красный', 'Красный "Сердолик" (195)', },
    'orange': {'Оранжевый "Марс" (130)', 'оранжевый'},
    'yellow': {'желтый', },
    'green': {'зеленый', },
    'cyan': {'голубой', },
    'blue': {'синий', 'Ярко-синий "Дайвинг" (476)'},
    'purple': {'фиолетовый', 'вишня', },
    'white': {'Белый "Ледниковый" (221)', },
    'black': {'Черный "Маэстро" (653)'},
    'brown': {'Коричневый "Ангкор" (246)'},
    'gray': {'Коричневый "Ангкор" (246)', 'Серо-бежевый "Карфаген" (247)', 'Серый "Плутон" (608)'},
    'lightsteelblue': {'Серо-голубой "Фантом" (496)'},
    'lightgrey': {'Серебристый "Платина" (691)'}
}


def get_color(c):
    res = [k for (k, v) in color_map.items() if c in v]
    return res[0] if res else 'midnightblue'

def get_color_car_icon(c):
    color = get_color(c)
    return f'<i class="fa fa-car fa-2x" style="color:{color}"></i>'
