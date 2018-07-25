"""
    This module will serve as an api for the DB
"""

import db.session as session
import db.model as model


def initialize():
    session.initialize()


def create_tables():
    model.objTable.metadata.create_all(session.ENGINE)


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


@session.ensure_session
def add_pack(pack, session=None):
    """Add a package to the DB"""
    test_pack(pack)
    package = model.objTable(pack)
    return package.save()


@session.ensure_session
def get_pack(id_node=None, session=None):
    """
        returns a result as a list
        containing all objects in the table with that id_node
    """
    query = session.query(model.objTable)
    result_query = query.filter(model.objTable.node_id == id_node)

    result = []
    for pack in result_query:
        result.append(pack.to_dict())

    return result
