#!/usr/bin/env python
from flask import Flask, jsonify, request
import pika
import uuid
import json
import server

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"about" : "bonjour, request exmaple explained:"+
                                "sitename/params?id_node=..."})

@app.route('/params')
def index2():
    recived_args = request.args

    if("id_node" not in recived_args):
        return "missing id_node"

    result = server.solve_request_from_api(recived_args['id_node'])
    return jsonify(result)



if __name__ == '__main__':
    server.main()
    app.run(debug=True, use_reloader=False)
