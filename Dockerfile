FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./tests /code/tests
COPY ./pytest.ini /code/pytest.ini


ENV PORT=80
ENV HOST=0.0.0.0

CMD uvicorn app.main:app --host ${HOST} --port ${PORT}