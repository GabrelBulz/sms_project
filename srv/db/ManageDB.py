"""
    This module will serve as an api for the DB
"""

import db.Session as Session
import db.Model as Model


def initialize():
    Session.initialize()


def create_tables():
    Model.objTable.metadata.create_all(Session.ENGINE)


def test_pack(pack):
    if 'id_node' in pack:
        if not isinstance(pack['id_node'], int):
            raise Exception('id_node not in correct format')
    else:
        raise Exception('missing id_node')

    if 'metrics' in pack:
        if not isinstance(pack['metrics'], dict):
            raise Exception('metrics not in correct format')
    else:
        raise Exception('missing metrics')


@Session.ensure_session
def add_pack(pack, session=None):
    """Add a package to the DB"""
    test_pack(pack)
    package = Model.objTable(pack)
    return package.save()


@Session.ensure_session
def get_pack(id_node=None, session=None):
    """
        returns a result as a list
        containing all objects in the table with that id_node
    """
    query = session.query(Model.objTable)
    result_query = query.filter(Model.objTable.node_id == id_node)

    result = []
    for pack in result_query:
        result.append(pack.to_dict())

    return result
