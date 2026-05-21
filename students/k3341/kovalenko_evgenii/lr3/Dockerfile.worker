from python:3.10-slim

workdir /code

copy ./app/requirements.txt /code/requirements.txt
run pip install --no-cache-dir -r requirements.txt

copy ./app /code

env PYTHONPATH=/code