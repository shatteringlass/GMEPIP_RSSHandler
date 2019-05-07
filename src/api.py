from flask import jsonify
from flask_restful import Resource

from .db import orm
from .models import Outage
from .pip_handler import GMEPIPRssHandler


class OutageEndpoint(Resource):
    @orm.db_session
    def get(self):
        GMEPIPRssHandler().to_db()
        d = [{k: str(getattr(x, k)) for k in x._columns_}
             for x in Outage.select().order_by(orm.desc(Outage.publication_dt))]
        return jsonify(d)
