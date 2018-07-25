#!/usr/bin/env python

"""
    Holds the flask server for the application
"""

from flask import Flask, jsonify, request
import server

APP = Flask(__name__)


@APP.route('/')
def index():
    """ Handles the default route """

    return jsonify({"about": "bonjour, request exmaple explained:" +
                             "sitename/params?id_node=..."})


@APP.route('/params')
def index2():
    """Handles the params route """
    recived_args = request.args

    if "id_node" not in recived_args:
        return jsonify("missing id_node")

    result = server.solve_request_from_api(recived_args)
    return jsonify(result)


if __name__ == '__main__':
    server.main()
    APP.run(debug=True, use_reloader=False)
