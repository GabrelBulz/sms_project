#!/usr/bin/env python

"""
    This module serves as a server for the app
    It handles the incomming packages from the client
    It initialize the DB
"""

import json
from threading import Thread
import pika
import db.ManageDB as ManageDb
import ConfigParserSERVER as ConfParsSRV

CONFIG = ConfParsSRV.ConfigMachineSRV('conf.ini')
CONFIG.parse_conf()


ManageDb.initialize()
ManageDb.create_tables()


class threadConClientServer(Thread):

    """
        Thread class for pika server

        create a pika connection, currently set to local host
        and start listen to that queue

        If a pack is recived it is added to DB
    """

    def __init__(self):
        Thread.__init__(self)

        """
        the pika connection can be created using the
        parameters from the config file
        with config.ampq_url and so,
        but fow now i'll just use local host

        cred = pika.PlainCredentials(CONFIG.ampq_user, CONFIG.ampq_password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=CONFIG.ampq_url,
            port=int(CONFIG.ampq_port),
            virtual_host=CONFIG.ampq_vhost,
            credentials=cred))
        """
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='client_server_ampq')

    def solve_queue(self, channel, method, properties, body):
        ManageDb.add_pack(json.loads(body))

    def run(self):
        self.channel.basic_consume(self.solve_queue,
                                   queue='client_server_ampq',
                                   no_ack=True)

        self.channel.start_consuming()


def solve_request_from_api(id_node):
    return ManageDb.get_pack(id_node)


def main():

    # create and start thread for pika connection
    thread_client_srv = threadConClientServer()
    thread_client_srv.start()


if __name__ == '__main__':
    main()
