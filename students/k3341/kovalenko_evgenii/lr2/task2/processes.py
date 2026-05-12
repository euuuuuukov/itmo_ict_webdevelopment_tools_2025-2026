from multiprocessing import Pool
from requests import get
from bs4 import BeautifulSoup
from sqlmodel import Session, select
from time import time

from pathlib import Path
from sys import path


path.insert(0, str(Path(__file__).parent.parent.parent / 'lr1' / 'lr'))


from students.k3341.kovalenko_evgenii.lr1.lr.connection import engine
from students.k3341.kovalenko_evgenii.lr1.lr.models import Category, User, Task, TaskCategoryLink, TaskStatus


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


def parse_and_save(url):
    soup = BeautifulSoup(get(url).text, 'html.parser')
    if soup.title:
        title = soup.title.string.strip()
    else:
        title = 'no title'

    with Session(engine) as session:
        task = Task(title=title, description=url, owner_id=session.exec(select(User)).first().id, status=TaskStatus.PENDING)
        session.add(task)
        session.commit()
        session.refresh(task)

        session.add(TaskCategoryLink(task_id=task.id, category_id=session.exec(
            select(Category).where(Category.name == 'web parsing')).first().id))
        session.commit()

        print(f'task_id {task.id}: {url} - {title}')


def main():
    with Pool(processes=4) as pool:
        for i in range(0, 8, 2):
            pool.map(parse_and_save, URLS[i:i + 2])


if __name__ == '__main__':
    start_time = time()
    main()
    print(f'threads: {time() - start_time} s')
