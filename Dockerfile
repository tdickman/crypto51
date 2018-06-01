FROM        ubuntu:18.04

ENV         PYTHONPATH=/app

RUN         apt update && apt install -y curl gnupg && rm -rf /var/lib/apt/lists/*
RUN         echo "deb http://packages.cloud.google.com/apt cloud-sdk-bionic main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN         curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

RUN         apt update && apt install -y google-cloud-sdk python3.6 python2.7 python3-pip g++ gcc libxslt-dev libffi-dev && rm -rf /var/lib/apt/lists/*
RUN         pip3 install pipenv

ENV         LC_ALL=C.UTF-8
ENV         LANG=C.UTF-8
ADD         Pipfile /tmp
ADD         Pipfile.lock /tmp

RUN         cd /tmp && pipenv install --system --python 3.6

WORKDIR     /app
COPY        . /app

CMD         ["/bin/bash", "-c", "gcloud auth activate-service-account --key-file /var/secrets/google/key.json && ./update.sh noprompt"]
