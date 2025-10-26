#!/bin/bash

set -e
export $(grep -v '^#' .env | xargs)

pushd .

cd dist

sudo nginx -c $(pwd)/nginx.conf
java -Xmx2G -Xms256m -jar backend.jar &
cd ai
source .venv/bin/activate
uvicorn main:app; fg

wait
popd

