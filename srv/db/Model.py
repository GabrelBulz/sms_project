import json
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime
import db.Session as Session


Base = declarative_base()
#id_cont = 0


"""
    Object to be stored it table

    It contains an
    id (to identify the added packages) incemented each time a pack is added
    node_id (id of node that sent the package)
    metrics
    timeStamp
"""
class objTable(Base):

    __tablename__ = 'tableMetrics'

    id = Column('id', Integer, primary_key=True)
    node_id = Column('node_id', Integer, unique=False, default=0)
    storedMetrics = Column('Metrics', String(200), default="missing metrics")
    TimeSpamp = Column('TimeStamp', DateTime, default=datetime.datetime.now)

    def __init__(self, pack):
        #global id_cont
        #id_cont+=1
        #self.id=id_cont

        try:
            self.node_id = pack['id_node']
            self.storedMetrics = str(pack['metrics'])
            self.TimeStamp = pack['timeStamp']
        except Exception as e:
            print("missing something from pack")


    @Session.ensure_session
    def save(self, session=None):
        print("obj"+str(self.to_dict()))
        session.add(self)
        session.flush()
        session.refresh(self)



    def to_dict(self):
        pack = {}

        pack['id'] = self.id
        pack['id_node'] = self.node_id;
        pack['metrics'] = self.storedMetrics
        pack['timeStamp'] = self.TimeSpamp

        return pack