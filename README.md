This project gathers data from a few different apis to calculate the estimated
cost of completing a theoretical 51% attack on a cryptocurrency network. It is
a python app that renders this data in jinja templated html files for hosting
on a static hosting service like Google Cloud Buckets, or AWS S3.

# Environment Setup / Running

Run the following to generate updated html files in the dist/ directory:

```
pipenv --python 3.6 shell
pipenv install
python app.py
python render.py
```

Alternatively you can run the following to generate updated html files + copy them to Google Cloud

```
pipenv --python 3.6 shell
pipenv install
./update.sh
```

# Dependencies

* pipenv
* python 3.6
