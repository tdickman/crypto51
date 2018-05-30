rm -rf dist/
mkdir dist/
mkdir dist/coins/
python crypto51attack/app.py
python crypto51attack/render.py
if [ "$1" != "noprompt" ]; then
    read -p "Please check the output and then press [ENTER] to continue"
fi
gsutil defacl set public-read gs://www.crypto51.app
gsutil -h "Cache-Control:public, max-age=600" -m rsync -d -r dist/ gs://www.crypto51.app/
