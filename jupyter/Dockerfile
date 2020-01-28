FROM python:3.7-slim-buster

ARG PW="andi_jupyter"
ENV PW=$PW

RUN pip install --upgrade pip && pip install pipenv
RUN apt-get update &&  apt-get install -yq \
    git \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/betagouv/andi-data/ /jupyter
WORKDIR /jupyter
RUN pipenv install --system --deploy
COPY ./start.sh /jupyter/start.sh

ENTRYPOINT [ "/jupyter/start.sh", "$PW"]
