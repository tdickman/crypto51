FROM    python:3.6-alpine

RUN     apk add --update g++ gcc libxslt-dev && rm -rf /var/cache/apk/*
RUN     pip install pipenv

ADD     Pipfile /tmp
ADD     Pipfile.lock /tmp

RUN     cd /tmp && pipenv install --system

WORKDIR /app
COPY    . /app

CMD     ["./update.sh", "noprompt"]
