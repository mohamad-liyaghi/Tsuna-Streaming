FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /backend

RUN pip install --upgrade pip 

COPY requirement.txt /backend

RUN pip install -r requirement.txt

COPY . /backend

RUN mv .env.prod.sample .env.prod

EXPOSE 8000