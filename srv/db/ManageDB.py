import db.Session as Session
import db.Model as Model


def initialize():
    Session.initialize()


def create_tables():
    Model.objTable.metadata.create_all(Session.engine)


@Session.ensure_session
def add_pack(pack, session=None):
    package = Model.objTable(pack)
    return package.save()