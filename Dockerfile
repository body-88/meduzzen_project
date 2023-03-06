FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/code"

CMD python app/runserver.py