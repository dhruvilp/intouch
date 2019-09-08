from flask import Flask
from flask import request
from flask import make_response
import common
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import logging
from linkedin import LinkedIn
import twilio_client

logging.getLogger().setLevel(logging.INFO)

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

if __name__ == '__main__':
    # This is used when running locally only.
    cred = credentials.Certificate('intouch-6a524-e13e8300153d.json')
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
    auth_code = content.get('auth_code', '')
    name = content.get('name', '')
    phone_number = content.get('phone_number', '')
    if not all([id, auth_code, name, phone_number]):
        logging.info("[new_user] missing name, auth_code, id, or phone_number")
        return error_code(400, "Must passed id, name, auth_code, phone_number")
    li = LinkedIn()
    access_token = "foo"  # li.getAccessToken(auth_code)
    db = get_database()
    doc_ref = db.collection(id).document("metadata")
    data = {'name': name, 'access_token': access_token, 'phone_number': phone_number}
    resp = new_doc(doc_ref, data)
    if resp.status_code == 200:
        doc_ref = db.collection("collections").document("metadata")
        doc_ref.update({'names': firestore.ArrayUnion([id])})
    return resp


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
        data["time_since_last_contact"] = frequency
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


@app.route(common.PATHS.GET_CONNECTION, methods=["POST"])
def get_connection():
    content = request.json
    id = content.get('id', None)
    connection_name = content.get('connection_name', None)
    if not all([id, connection_name]):
        return error_code(400, "Must pass id and connection_name")
    db = get_database()
    doc = db.collection(id).document(connection_name).get()
    if not doc.exists:
        return error_code(400, "Unknown id or connection_name")
    resp_conts = doc.to_dict()
    resp_conts["id"] = id
    resp_conts["connection_name"] = connection_name
    return make_response(resp_conts, 200)


def _get_connections(db, collection):
    docs = []
    for doc in db.collection(collection).stream():
        doc_dict = doc.to_dict()
        if doc_dict.get('time_since_last_contact'):
            doc_dict["connection_name"] = doc.id
            docs.append(doc_dict)
    sorted(docs, key=lambda i: (i['time_since_last_contact'], i['connection_name']))
    ordered_docs = dict(zip(list(range(len(docs))), docs))
    return ordered_docs


@app.route(common.PATHS.GET_CONNECTIONS, methods=["POST"])
def get_connections():
    content = request.json
    id = content.get('id', None)
    if not id:
        return error_code(400, "Must pass id")
    db = get_database()
    docs = _get_connections(db, db.collection(id))
    return make_response(docs, 200)


def get_collections():
    db = get_database()
    names = db.collection("collections").document("metadata").get().to_dict().get('names', [])
    collections = []
    for name in names:
        collections.append(db.collection(name))
    return names


@app.route("/demo/notify", methods=["GET"])
def demo_notify():
    notify_to_contact_network()


def notify_to_contact_network():
    collections = get_collections()
    for collection in collections:
        db = get_database()
        connections = _get_connections(db, collection)
        time_to_speak = []
        past_deadline = []
        for connection in connections.values():
            if int(connection["time_since_last_contact"]) == 0:
                time_to_speak.append(connection)
            if int(connection["time_since_last_contact"]) < 0:
                past_deadline.append(connection)
        if time_to_speak or past_deadline:
            message = ["It's time to network!\n"]
            if time_to_speak:
                message.append("Today you should try and get in touch with: \n")
                for connection in time_to_speak:
                    message.append(connection["connection_name"] + "\n")
            if past_deadline:
                message.append("You're passed the deadline you set for speaking to: \n")
                for connection in past_deadline:
                    message.append(connection["connection_name"] + "\n")
            phone_number = db.collection(collection).document('metadata').get().get("phone_number")
            message = "".join(message)
            twilio_client.TwilioClient().send_text(phone_number, message)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

# [END gae_python37_app]
