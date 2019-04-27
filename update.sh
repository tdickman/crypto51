#!/bin/bash
set -e

rm -rf dist/
mkdir dist/
mkdir dist/coins/
python3 crypto51/app.py
python3 crypto51/render.py
if [ "$1" != "noprompt" ]; then
    read -p "Please check the output and then press [ENTER] to continue"
fi
# gsutil defacl set public-read gs://www.crypto51.app
# gsutil defacl set public-read gs://api.crypto51.app
gsutil -h "Cache-Control:public, max-age=600" -m rsync -d -r dist/ gs://www.crypto51.app/
gsutil -h "Cache-Control:public, max-age=600" cp dist/coins.json gs://api.crypto51.app/
gsutil -h "Cache-Control:public, max-age=600" cp dist/coins.json gs://api.crypto51.app/history/`date +%Y/%m/%d/%H-%M`.json
