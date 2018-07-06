from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import ConfigParser_db


config = ConfigParser_db.ConfigMachine_db('../conf.ini')
config.parse_conf()

Base = declarative_base()


class Pack_metrics (Base):

    __tablename__ = 'tableMetrics'

    id = Column('id', Integer, primary_key=True)
    node_id = Column('node_id', Integer, unique=False, default=0)
    storedMetrics = Column('Metrics', String(200), default="missing metrics")
    TimeSpamp = Column('TimeStamp', DateTime, default=datetime.datetime.now)

    def __init__(self, pack):

        try:
            self.node_id = pack['id_node']
            self.storedMetrics = pack['metrics']
            self.TimeStamp
        except Exception as e:
            print("missing something from pack")

    def save(self, session=None):




    def to_dict(seft):

        pack = {}

        pack['id_node'] = self.node_id;
        pack['metrics'] = self.storedMetrics
        pack['timeStamp'] = self.TimeStamp

        return pack


engine = create_engine('sqlite:///:memory:', echo=True)

if not engine.dialect.has_table(engine, 'tableMetrics'):
    Base.metadata.create_all(bind=engine)
    print("ffffffff")

Session = sessionmaker(bind=engine)

session = Session()

obj= session.query(Pack_metrics).all()

print(obj)


session.close()



