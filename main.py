import argparse
import json
import logging

from flask import Flask
from flask import request
from google.cloud import storage

import jinja2

import ds
import sms


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

@app.route('/send', methods=['POST'])
def sendSnapVite():
    data = json.loads(request.form.get('json'))

    message = 'Message from ' + data['username'] + ': ' + data['message']

    ds.insertSnapVite(data['username'], message, data['recipients'])
    return 'foo'

    response = 'SMS sent to: '
    for recipient in data['recipients']:
        if recipient == 'Jim':
            sms.send(message, '+12063567329')
        elif recipient == 'Kacy':
            sms.send(message, '+12062274548')
        response += recipient + ' '
    return response

@app.route('/show/<snapvite_id>')
def showSnapVite(snapvite_id):
    return ds.retrieve(snapvite_id)


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



