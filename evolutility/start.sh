#!/bin/bash
echo -e "DANGEROUSLY_DISABLE_HOST_CHECK=true\n" > /src/ui/.env.development.local
pm2 start ./server/bin/www
cd ./ui
ls -lah
serve -s build -l 3000
# npm start
