import json
from flask import Flask
from flask import request
from flask import Response

import users

app = Flask(__name__)


# GET - Returns user info
@app.route('/users/<phone_number>', methods=['GET'])
def http_users_get(phone_number=None):
    try:
        response = users.get(phone_number)
    except Exception as err:
        response = {'code': 500, 'message': 'main.py:users_get - ' + str(err)}
    return json.dumps(response), int(response['code'])


# POST - Creates a new user, and sends registration code via SMS message
@app.route('/users', methods=['POST'])
def http_users_create():
    try:
        response = users.create(request)
    except Exception as err:
        response = {'code': 500, 'message': 'main.py:users_create - ' + str(err)}
    return json.dumps(response), int(response['code'])


# PATCH - Updates user account, either registration code or new username
@app.route('/users', methods=['PATCH'])
def http_users_update():
    try:
        response = users.update(request)
    except Exception as err:
        response = {'code': 500, 'message': 'main.py:users_update - ' + str(err)}
    return json.dumps(response), int(response['code'])

# DELETE - Deletes a user from a given item
@app.route('/items_users/<item_id>/<phone_number>', methods=['DELETE'])
def http_items_users_delete(item_id, phone_number):
    try:
        response = items_users.delete(item_id, phone_number)
    except Exception as err:
        response = {'code': 500, 'message': 'main.py:items_users_delete - ' + str(err)}
    return json.dumps(response), int(response['code'])


#############################################################################
# For DEBUG execution on local server only.  
# On prod server, all of these requests should be handled by nginx
#############################################################################

@app.route('/')
def http_home():
    return http_web('snapvite.html')

@app.route('/web/<file_name>')
def http_web(file_name):
    f = open('../web/' + file_name, 'r')
    if 'css' in file_name:
        return Response(f.read(), mimetype='text/css')
    if 'js' in file_name:
        return Response(f.read(), mimetype='text/javascript')
    return f.read()

@app.route('/web/external/<file_name>')
def http_external(file_name):
    f = open('../web/external/' + file_name, 'r')
    if 'css' in file_name:
        return Response(f.read(), mimetype='text/css')
    if 'js' in file_name:
        return Response(f.read(), mimetype='text/javascript')
    return f.read()

@app.route('/images/icons/<file_name>')
def http_icons(file_name):
    try:
        f = open('../web/images/icons/' + file_name, 'rb')
        return f.read()
    except Exception as err:
        print(str(err))
    return ''

@app.route('/media/<file_name>')
def http_media(file_name):
    try:
        f = open('../web/media/' + file_name, 'rb')
        return f.read()
    except Exception as err:
        print(str(err))
    try:
        f = open('../web/media/default.jpg', 'rb')
        return f.read()
    except Exception as err:
        print(str(err))
    return ''

@app.route('/media/items/<file_name>')
def http_media_items(file_name):
    try:
        f = open('../web/media/items/' + file_name, 'rb')
        return f.read()
    except Exception as err:
        print(str(err))
    try:
        f = open('../web/media/default.jpg', 'rb')
        return f.read()
    except Exception as err:
        print(str(err))
    return ''

@app.route('/media/users/<file_name>')
def http_media_users(file_name):
    try:
        f = open('../web/media/users/' + file_name, 'rb')
        return f.read()
    except Exception as err:
        print(str(err))
    try:
        f = open('../web/media/default.jpg', 'rb')
        return f.read()
    except Exception as err:
        print(str(err))
    return ''

#############################################################################
#############################################################################


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

# Command line to run with gunicorn
#   gunicorn -w 24 -b 0.0.0.0:8080 --log-level=debug main:app

