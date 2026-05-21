from celery import Task
from httpx import Client, RequestError
from celery_app import celery_app


class ParseTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(f'task {task_id} failed: {exc}')


@celery_app.task(base=ParseTask, bind=True, max_retries=3)
def parse_task(self, urls: list[str], user_id: int):
    try:
        with Client(timeout=30) as client:
            resp = client.post('http://parser:8001/parse', json={'urls': urls, 'user_id': user_id})
            resp.raise_for_status()
            return {'status': 'success', 'response': resp.json()}
    except RequestError as e:
        self.retry(exc=e, countdown=60)
        raise