FROM python:3.6-slim

COPY ./app /code/app
COPY ./settings /code/settings
COPY ./resources /code/resources
COPY ./Pipfile /code
COPY ./Pipfile.lock /code

WORKDIR /code
RUN pip install pipenv
RUN pipenv install --system -d --ignore-pipfile
