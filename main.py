from flask import Flask
from flask import request
from flask import make_response
import common
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import google
import logging

logging.getLogger().setLevel(logging.INFO)

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

if __name__ == '__main__':
    # This is used when running locally only.
    cred = credentials.Certificate('intouch-6a524-8ba1874aba3b.json')
    firebase_admin.initialize_app(cred)
else:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': common.PROJECT_ID,
    })


def get_database():
    db = firestore.client()
    return db


def error_code(code, error):
    resp = make_response("ERROR", code)
    resp.reason = error
    return resp


def OK():
    resp = make_response("OK", 200)
    return resp


@app.route('/')
def root():
    """Return response for route"""
    return 'This is the backend server for InTouch.'


@app.route(common.PATHS.NEW_USER, methods=["POST"])
def new_user():
    content = request.json
    logging.info("[new_user] got request with content %s" % str(content))
    id = content.get('id', '')
    name = content.get('name', '')
    if not id or not name:
        return error_code(400, "Must pass id and name")
    db = get_database()
    doc_ref = db.collection(id).document("metadata")
    doc = doc_ref.get()
    if doc.exists:
        return error_code(409, "id already exists in database")
    doc_ref.set(content)
    return OK()


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

# [END gae_python37_app]
