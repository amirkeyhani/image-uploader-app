FROM python:3.10.4
LABEL MAINTAINER="Amir Keyhani | https://amir.key_"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /imageuploader
WORKDIR /imageuploader
COPY . /imageuploader

ADD requirements.txt /imageuploader
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python manage.py collectstatic --no-input

CMD ["gunicorn", "--chdir", "imageuploader", "--bind", ":8000", "imageuploader.wsgi:application"]