#!/bin/bash
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")   

pushd .

export VITE_BASE='/app'

cd $SCRIPT_DIR

cd frontend
bun install
bun run build

cd ../backend
mvn install -DskipTests
mvn clean package -DskipTests

cd $SCRIPT_DIR

cd growthway-landing
bun install
bun run build

cd $SCRIPT_DIR

rm -rf dist
mkdir -pv dist/static
mkdir -pv dist/ai

cp -v backend/target/backend*.jar dist/backend.jar
cp -vr growthway-landing/dist/ "dist/static"
cp -vr frontend/dist/ "dist/static$VITE_BASE"
cp -vr ai/* dist/ai
cp nginx.conf dist/nginx.conf
cp proxy_params dist/

cd dist/ai
python -m venv ./.venv
source .venv/bin/activate
pip install -r requirements.txt

cd $SCRIPT_DIR

popd .
