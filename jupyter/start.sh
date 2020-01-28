#!/bin/bash
export PASW=`python -c "from notebook.auth import passwd; print(passwd('$PW'))"`
jupyter notebook -y \
    --allow-root \
    --ip=0.0.0.0 \
    --port=45000 \
    --notebook-dir=/notebooks \
    --no-browser \
    --NotebookApp.base_url='/jupyter' \
    --NotebookApp.password=$PASW
