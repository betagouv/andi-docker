FROM node:9

ARG PG_USER="user"
ARG PG_PASS="secret"
ARG PG_HOST="database"
ARG PG_PORT="54320"
ARG PG_DB="andi_entreprises"
ENV DATABASE_URL=postgres://$PG_USER:$PG_PASS@$PG_HOST:$PG_PORT/$PG_DB

# RUN apk update && apk upgrade && \
#     apk add --no-cache bash git openssh

RUN mkdir /src
WORKDIR /src


RUN echo "Cloning evolutility source.." && \
    # git clone https://github.com/evoluteur/evolutility-server-node.git ./server
    git clone --single-branch --branch faster_count https://github.com/PieterjanMontens/evolutility-server-node.git ./server

RUN npm install pm2@latest -g && \
    npm install serve@latest -g
 
WORKDIR /src/server
RUN npm install


WORKDIR /src
COPY ./server/config.js /src/server/config.js
COPY ./server/*.js /src/server/models/

WORKDIR /src/server
# ENTRYPOINT ["/bin/bash"]
ENTRYPOINT ["npm", "start"]
