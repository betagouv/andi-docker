FROM python:alpine3.7

ARG AIRTABLE_KEY="nope"
ARG AIRTABLE_BASE_KEY="nope"
ARG MG_BOX="nope"
ARG MG_KEY="nope"
ARG PG_DSN="postgres://[user]:[pass]@[host]:[port]"

ENV AIRTABLE_KEY=$AIRTABLE_KEY
ENV AIRTABLE_BASE_KEY=$AIRTABLE_BASE_KEY
ENV MG_BOX=$MG_BOX
ENV MG_KEY=$MG_KEY
ENV PG_DSN=$PG_DSN

RUN pip install --upgrade pip && pip install pipenv
RUN apk add --no-cache bash postgresql-dev alpine-sdk && \
    pip install --upgrade pip setuptools 'pipenv'

COPY . /app
WORKDIR /app
RUN pipenv install --system --deploy

# ENTRYPOINT ["bash"]
ENTRYPOINT ["./sendbot.py"]
