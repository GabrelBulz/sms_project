"""
    servre as a model for an object that will be stored in the DB
"""

import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import server_sms_proj.db.session as session


BASE = declarative_base()


class objTable(BASE):

    """
        Object to be stored it table

        It contains an
        id(to identify the added packages) incemented each time a pack is added
        node_id (id of node that sent the package)
        metrics
        timeStamp

    """

    __tablename__ = 'table_metrics'

    id = Column('id', Integer, primary_key=True)
    node_id = Column('node_id', Integer, unique=False, default=0)
    stored_metrics = Column('metrics', String(200), default="missing metrics")
    time_stamp = Column('time_stamp', String(200), default=str(datetime.datetime.now))

    def __init__(self, pack):
        try:
            self.node_id = pack['id_node']
            self.stored_metrics = str(pack['metrics'])
            self.time_stamp = pack['time_stamp']
        except Exception:
            print("missing something from pack")

    @session.ensure_session
    def save(self, session=None):
        session.add(self)
        session.flush()
        session.refresh(self)

    def to_dict(self):
        pack = {}

        pack['id'] = self.id
        pack['id_node'] = self.node_id
        pack['metrics'] = self.stored_metrics
        pack['time_stamp'] = self.time_stamp

        return pack
