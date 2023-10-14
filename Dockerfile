FROM python:3.11
LABEL authors="igor"

COPY ./requirements.txt /src/requirements.txt
RUN pip3 install -r /src/requirements.txt
COPY . /src
WORKDIR src