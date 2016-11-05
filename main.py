import argparse
import logging

from flask import Flask
from google.cloud import storage

import jinja2


app = Flask(__name__)
run_local = False

def fetch():
    if run_local:
        index_html = open('index.html', 'r').read()
    else:
        client = storage.Client('snapvite-app')
        bucket = client.get_bucket('snapvite')
        index_html = bucket.get_blob('index.html').download_as_string().decode('UTF-8')

    return jinja2.Template(index_html).render()

def upload_html():
    client = storage.Client('snapvite-app')
    bucket = client.get_bucket('snapvite')
    bucket.blob('index.html').upload_from_filename(filename='index.html')

@app.route('/')
def home():
    return fetch()


# This is used when running locally. Gunicorn is used to run the
# application on Google App Engine. See entrypoint in app.yaml.
if __name__ == '__main__':
    run_local = True

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--upload', help='Upload local html files to Cloud Storage', action='store_true')
    args = parser.parse_args()
    if args.upload:
        upload_html()
        print('All files uploaded to Cloud Storage')
    else:
        app.run(host='127.0.0.1', port=8080, debug=True)



