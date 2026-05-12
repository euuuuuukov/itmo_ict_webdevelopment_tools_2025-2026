from asyncio import run
from asyncpg import connect
from sqlmodel import Session
from time import time

from pathlib import Path
from sys import path


path.insert(0, str(Path(__file__).parent.parent.parent / 'lr1' / 'lr'))


from students.k3341.kovalenko_evgenii.lr1.lr.models import Category
from students.k3341.kovalenko_evgenii.lr1.lr.config import DB_URL
from students.k3341.kovalenko_evgenii.lr1.lr.connection import engine

def sync_connect():
    with Session(engine) as session:
        session.add(Category(name='web parsing', description='web parsing'))
        session.commit()


async def async_connect():
    conn = await connect(DB_URL)
    await conn.execute("insert into category (name, description) values ('web parsing', 'web parsing')")
    await conn.close()


if __name__ == '__main__':
    start_time = time()
    run(async_connect())
    print(f'async connect: {time() - start_time} s')

    start_time = time()
    sync_connect()
    print(f'sync connect: {time() - start_time} s')
