FROM python:3.6-slim

ADD ./app /code/app
ADD ./settings /code/settings
ADD ./resources /code/resources
ADD ./requirements.txt /code/requirements.txt

WORKDIR /code
RUN pip install -r requirements.txt
