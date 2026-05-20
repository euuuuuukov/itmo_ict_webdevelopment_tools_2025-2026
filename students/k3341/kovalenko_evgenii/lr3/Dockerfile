from python:3.10

workdir /code

copy ./app/requirements.txt /code/requirements.txt
run pip install --no-cache-dir -r requirements.txt

copy ./app /code

env PYTHONPATH=/code

cmd ['uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '8000']