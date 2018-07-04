from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import ConfigParser_db


class ManageDB(object):


    def __init__(self):
        self.config = ConfigParser_db.ConfigMachine_db('../conf.ini')
        self.config.parse_conf()

    def create_DB(self):
        engine = create_engine(self.config.url, echo=True)

    def getMetrics(self, reqest):

        print(reqest)

    def putMetrics(self, pack_metrics):

        print("put "+pack_metrics)

gg=ManageDB()
gg.create_DB()
