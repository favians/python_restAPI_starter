FROM python:3.7.5-slim-stretch

MAINTAINER Vian "Faviansyah"

WORKDIR /app

RUN mkdir storage && \
    mkdir storage/log && \
    touch storage/log/app.log

COPY . .

RUN pip install -r requirements.txt

CMD [ "python3", "app.py" ]

