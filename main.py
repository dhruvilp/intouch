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


def new_doc(doc_ref, content):
    doc = doc_ref.get()
    if doc.exists:
        return error_code(409, "id already exists in database")
    doc_ref.set(content)
    return OK()


def update_doc(doc_ref, content):
    doc = doc_ref.get()
    if not doc.exists:
        return error_code(424, "doc does not exist so can't be updated")
    doc_ref.update(content)
    return OK()


@app.route(common.PATHS.NEW_USER, methods=["POST"])
def new_user():
    content = request.json
    logging.info("[new_user] got request with content %s" % str(content))
    id = content.get('id', '')
    name = content.get('name', '')
    if not id or not name:
        logging.info("[new_user] missing name or id")
        return error_code(400, "Must pass id and name")
    db = get_database()
    doc_ref = db.collection(id).document("metadata")
    data = {'name': name}
    return new_doc(doc_ref, data)


def modify_connection(content, new=False, edit=False):
    if new == edit:
        return error_code(400, "Must be new or edit")
    id = content.get('id', None)
    connection_name = content.get('connection_name', None)
    frequency = content.get('frequency', None)
    how_you_met = content.get('how_you_met', None)
    their_challenges = content.get('their_challenges', None)
    other_notes = content.get('other_notes', None)
    if new and not all([id, connection_name, frequency, how_you_met, their_challenges, other_notes]):
        return error_code(400, "Must pass name, frequency, how_you_met, their_challenges, other_notes")
    if edit and not all([id, connection_name]):
        return error_code(400, "Must pass name, id")
    db = get_database()
    doc_ref = db.collection(id).document(connection_name)
    data = {'frequency': frequency,
            'how_you_met': how_you_met,
            'their_challenges': their_challenges,
            'other_notes': other_notes}
    if new:
        return new_doc(doc_ref, data)
    if edit:
        data = {k: v for k, v in data.items() if v is not None}
        return update_doc(doc_ref, data)


@app.route(common.PATHS.NEW_CONNECTION, methods=["POST"])
def new_connection():
    content = request.json
    logging.info("[new_connection] got request with content %s" % str(content))
    return modify_connection(content, new=True)


@app.route(common.PATHS.EDIT_CONNECTION, methods=["POST"])
def edit_connection():
    content = request.json
    logging.info("[edit_connection] got request with content %s" % str(content))
    return modify_connection(content, edit=True)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

# [END gae_python37_app]
