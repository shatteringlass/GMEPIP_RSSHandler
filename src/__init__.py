from flask import Flask
from flask_restful import Api

from .api import OutageEndpoint
from .db import SQLITE_DATAFILE
from .db import db

config = {
    'JSONIFY_PRETTYPRINT_REGULAR': True,
    'JSON_SORT_KEYS': False,
}

def build_app():
    app = Flask(__name__)
    api = Api(app)
    app.config.update(config)
    db.bind(provider='sqlite', filename=SQLITE_DATAFILE, create_db=True)
    db.generate_mapping(create_tables=True)
    api.add_resource(OutageEndpoint, '/umm')
    return app
