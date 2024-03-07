FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt /.
COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements.txt
RUN python manage.py collectstatic

EXPOSE 8000