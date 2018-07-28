#!/usr/bin/env python

"""
    This module serves as a server for the app
    It handles the incomming packages from the client
    It initialize the DB
"""

import json
import os
import sys
from threading import Thread
import pika
from server_sms_proj.db import manageDB as manageDb
from server_sms_proj import config_parser_server as ConfParsSRV
from server_sms_proj import filter_pack


manageDb.initialize()
manageDb.create_tables()


class ThreadConClientServer(Thread):

    """
        Thread class for pika server

        create a pika connection, currently set to local host
        and start listen to that queue

        If a pack is recived it is added to DB
    """

    def __init__(self, config):
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
        self.config = config
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='client_server_ampq')

    def solve_queue(self, channel, method, properties, body):
        try:
            manageDb.add_pack(json.loads(body))
        except Exception as exc:
            print('Not able to insert pack: ' + str(body) + str(exc))

    def run(self):
        self.channel.basic_consume(self.solve_queue,
                                   queue='client_server_ampq',
                                   no_ack=True)

        self.channel.start_consuming()


def set_up_config():
    """
        parse --config file from the command line
    """
    filename = 'default_conf.ini'

    if len(sys.argv) > 1:
        if sys.argv[1] == '--config':
            try:
                filename = str(sys.argv[2])
            except IndexError:
                print('missing filename or path after --config')

    if not os.path.isfile(filename):
        filename = 'default_conf.ini'
        print('given config path or file does not exist')

    config = ConfParsSRV.ConfigMachineSRV(filename)
    config.parse_conf()

    return config


def solve_request_from_api(received_args):
    """
        tries to apply the filter received from the api

        the only exception handeled is where the interval is not a numeric
        value  ---> a string is return if the error occurs
    """
    result = manageDb.get_pack(received_args['id_node'])
    try:
        filt = filter_pack.FilterPack(result, received_args)
        return filt.get_filtered_pack()
    except ValueError:
        return str('Invalid interval: cannot convert')


def main():
    config = set_up_config()

    # create and start thread for pika connection
    thread_client_srv = ThreadConClientServer(config)
    thread_client_srv.start()


if __name__ == '__main__':
    main()
