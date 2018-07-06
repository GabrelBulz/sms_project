#!/usr/bin/env python
from flask import Flask, jsonify, request
import pika
import uuid
import json

app = Flask(__name__)


class CommunicationSession(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, info_req):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=json.dumps(info_req))
        while self.response is None:
            self.connection.process_data_events()
        return "ok"


@app.route('/')
def index():
    return jsonify({"about" : "bonjour, request exmaple explained:"+
                                "sitename/params?id_node=...&metrics=...&interval=optional"+
                                "metrics will be written one after another with , between metrics"+
                                "ex: metrics=cpu_percent,virual_memory,disk_usage"+
                                "until now that are all the metrics implemented"})

@app.route('/params')
def index2():
    recived_args = request.args

    if("id_node" not in recived_args):
        return "missing id_node"

    if("metrics" not in recived_args):
        return "missing metrics"

    sesion = CommunicationSession()

    response = sesion.call(recived_args)
    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True)
