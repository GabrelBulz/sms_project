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


@Session.ensure_session
def get_pack(id_node=None, session=None):
    query = session.query(Model.objTable)
    result_query =  query.filter(Model.objTable.node_id == id_node)

    result = []
    for pack in result_query:
        result.append(pack.to_dict())

    return result
