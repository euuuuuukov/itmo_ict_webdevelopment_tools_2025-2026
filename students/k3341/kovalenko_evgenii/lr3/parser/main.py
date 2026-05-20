from fastapi import FastAPI, Body
from dotenv import load_dotenv
from os import getenv
from typing import List
from asyncpg import create_pool
from asyncio import gather, to_thread, create_task
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from datetime import datetime
from uvicorn import run


app = FastAPI(title='parser')

load_dotenv()
DB_URL = getenv('DB_URL')


async def get_cat_id(conn):
    return await conn.fetchval("select id from category where name = 'web parsing'")


async def parse_and_save(url, pool, cat_id, user_id):
    async with pool.acquire() as conn:
        async with ClientSession() as session:
            async with session.get(url) as resp:
                soup = await to_thread(BeautifulSoup, await resp.text(), 'html.parser')
                if soup.title:
                    title = soup.title.string.strip()
                else:
                    title = 'no title'

                task_id = await conn.fetchval("insert into task (title, description, owner_id, status, priority, estimated_hours, total_spent_hours, created_at) values ($1, $2, $3, $4, $5, $6, $7, $8) returning id", title, url, user_id, 'PENDING', 'MEDIUM', 1.0, 0.0, datetime.now())
                await conn.execute('insert into taskcategorylink (task_id, category_id, assigned_at) values ($1, $2, $3)', task_id, cat_id, datetime.now())

                return {'url': url, 'title': title, 'task_id': task_id}


@app.post('/parse')
async def parse(data: dict):
    async def run_parsing():
        pool = await create_pool(DB_URL, min_size=1, max_size=10)
        try:
            async with pool.acquire() as conn:
                cat_id = await get_cat_id(conn)

            tasks = [parse_and_save(url, pool, cat_id, data.get('user_id')) for url in data.get('urls')]
            await gather(*tasks)
        finally:
            await pool.close()

    create_task(run_parsing())
    return {'message': 'parsing started'}


if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8001)
