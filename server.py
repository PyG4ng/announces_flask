from flask import Flask, jsonify, request
from flask.views import MethodView

from crud import get_announce, create_announce, patch_announce, delete_announce
from db import Session
from errors import HttpError, error_handler
from models import Announce
from schema import CreateAnnounce, PatchAnnounce, validate

app = Flask('app')


class UserView(MethodView):

    def get(self, announce_id: int):
        with Session() as session:
            announce = get_announce(session, Announce, announce_id)
            return jsonify({'id': announce.id, 'announce_title': announce.title,
                            'announce_author': announce.author,
                            'creation_time': announce.creation_time.isoformat()})

    def post(self):
        json_data = validate(request.json, CreateAnnounce)
        with Session() as session:
            announce = create_announce(session, Announce, json_data)
            return jsonify({'status': 'created', 'id': announce.id, 'announce_title': announce.title,
                            'announce_author': announce.author})

    def patch(self, announce_id: int):
        json_data = validate(request.json, PatchAnnounce)
        with Session() as session:
            announce = get_announce(session, Announce, announce_id)
            announce = patch_announce(session, announce, json_data)
            return jsonify({'status': 'patched', 'announce_id': announce.id, 'announce_title': announce.title,
                            'announce_author': announce.author})

    def delete(self, announce_id: int):
        with Session() as session:
            announce = get_announce(session, Announce, announce_id)
            delete_announce(session, announce)
            return jsonify({'status': 'deleted', 'announce_id': announce.id, 'announce_title': announce.title,
                            'announce_author': announce.author})


app.add_url_rule('/announce/<int:announce_id>', view_func=UserView.as_view('announce'),
                 methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/announce/', view_func=UserView.as_view('announce_create'), methods=['POST'])

app.errorhandler(HttpError)(error_handler)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
