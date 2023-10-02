FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /backend
ENV PYTHONPATH=/backend

RUN pip install --upgrade pip 

COPY backend/requirement.txt /backend

RUN pip install -r requirement.txt

COPY /backend /backend



EXPOSE 8000