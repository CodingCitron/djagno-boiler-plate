FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get update
RUN apt-get install -y ffmpeg
ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt