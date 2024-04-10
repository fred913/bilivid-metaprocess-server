FROM python:3.10-slim-bullseye

RUN mkdir /app

COPY Pipfile /app
COPY acrcloud_sdk_python /app/acrcloud_sdk_python

WORKDIR /app

RUN apt update && apt install git aria2 ffmpeg -y && pip install pipenv && pipenv update && rm -rf /var/lib/apt/lists/* 

WORKDIR /app/acrcloud_sdk_python
RUN pipenv run python setup.py install

WORKDIR /app

COPY . /app/

EXPOSE 8000

ENTRYPOINT [ "pipenv", "run", "python", "runapp.py" ]