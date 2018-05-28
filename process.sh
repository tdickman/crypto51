python crypto51attack/app.py
python crypto51attack/render.py
gsutil defacl set public-read gs://www.crypto51.app
gsutil -m rsync -d -r dist/ gs://www.crypto51.app/
