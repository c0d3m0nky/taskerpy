FROM python:3.9

WORKDIR /code

COPY ./src /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD echo '---> pip pip hooray' && pip install --no-cache-dir --upgrade -r /code/requirements.txt && echo '---> starting api' && uvicorn main:app --host 0.0.0.0 --port 80
