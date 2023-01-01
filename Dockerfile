FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /backend

RUN pip install --upgrade pip 

COPY requirement.txt /backend

RUN pip install -r requirement.txt

COPY . /backend

EXPOSE 8000