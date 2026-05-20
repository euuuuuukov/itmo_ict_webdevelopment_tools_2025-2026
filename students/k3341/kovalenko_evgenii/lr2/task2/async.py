from asyncio import to_thread, gather, run
from aiohttp import ClientSession
from asyncpg import create_pool
from bs4 import BeautifulSoup
from time import time
from datetime import datetime

from pathlib import Path
from sys import path


path.insert(0, str(Path(__file__).parent.parent.parent / 'lr1' / 'lr'))


from students.k3341.kovalenko_evgenii.lr1.lr.config import DB_URL


URLS = [
    'https://www.python.org/',
    'https://www.github.com/',
    'https://stackoverflow.com/',
    'https://www.wikipedia.org/',
    'https://news.ycombinator.com/',
    'https://www.reddit.com/',
    'https://habr.com/',
    'https://www.yahoo.com/'
]


async def parse_and_save(url, session, pool):
    async with pool.acquire() as conn:
        async with session.get(url) as resp:
            soup = await to_thread(BeautifulSoup, await resp.text(), 'html.parser')
            if soup.title:
                title = soup.title.string.strip()
            else:
                title = 'no title'

            cat_id = await conn.fetchval("select id from category where name='web parsing'")
            user_id = await conn.fetchval('select id from \"user\" limit 1')
            task_id = await conn.fetchval("insert into task (title, description, owner_id, status, priority, estimated_hours, total_spent_hours, created_at) values ($1, $2, $3, $4, $5, $6, $7, $8) returning id", title, url, user_id, 'PENDING', 'MEDIUM', 1.0, 0.0, datetime.now())
            await conn.execute('insert into taskcategorylink (task_id, category_id, assigned_at) values ($1, $2, $3)', task_id, cat_id, datetime.now())

            print(f'task_id {task_id}: {url} - {title}')


async def main():
    pool = await create_pool(DB_URL, min_size=1, max_size=10)
    async with ClientSession() as session:
        tasks = [parse_and_save(url, session, pool) for url in URLS]
        await gather(*tasks)
    await pool.close()


if __name__ == '__main__':
    start_time = time()
    run(main())
    print(f'async: {time() - start_time} s')