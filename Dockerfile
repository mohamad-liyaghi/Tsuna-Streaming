FROM python:3.11.2-alpine3.17

ENV PYTHONUNBUFFERED=1

WORKDIR /backend

RUN pip install --upgrade pip 

COPY requirement.txt /backend

RUN pip install -r requirement.txt

COPY . /backend

EXPOSE 8000