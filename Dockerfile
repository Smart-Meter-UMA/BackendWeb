FROM python:3.10.8-alpine3.15

WORKDIR /app

RUN apk update \
    && apk add --no-cache gcc musl-dev python3-dev libffi-dev \
    && pip install --upgrade pip 

COPY ./requirements.txt ./

RUN pip install psycopg2-binary
RUN pip install django-environ


RUN pip install -r requirements.txt

COPY ./ ./

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8001"]