#!/usr/bin/env python

"""
    Sys args
        --config -filename- or -path-

    This module will create a pika connection to the server
    CURRENTLY THE PIKA CONNECTION IS MADE USING LOCALHOSt, but ca be modified
    to use the credentials, and port for the CONFIG param

    A package containing:
    -id_node
    -metrics collected
    -time stamp
    will be created and send to the server based on the interval from the
    config file
"""

import os
import sys
import time
import pika
from client_sms import collector
from client_sms import config_parser


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

    config = config_parser.ConfigMachine(filename)
    config.parse_conf()

    return config


"""
the pika connection can be created using the
parameters from the config file
with config.ampq_url and so,
but fow now i'll just use local host

CREDENTIALS = pika.PlainCredentials(CONFIG.ampq_user, CONFIG.ampq_password)
CONNECTION = pika.BlockingConnection(pika.ConnectionParameters(
    host=CONFIG.ampq_url,
    port=int(CONFIG.ampq_port),
    virtual_host=CONFIG.ampq_vhost,
    credentials=CREDENTIALS))
"""
def create_pika_connection(config):
    """
        creates and returns a channel to pika connection

        config param should be used when creating connection if needed
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='client_server_ampq')

    return channel


def send_metrics(channel_pika, config):
    """
        this function will create a json object to be sent to the server
        it will contain the id_node , the collected metrics, and the interval
    """
    pack_collected = collector.Collector(config.id_node, config.metrics)
    pack_collected.collect_metrics()

    channel_pika.basic_publish(exchange='',
                               routing_key='client_server_ampq',
                               body=pack_collected.to_json())


def main():

    config = set_up_config()
    channel_pika = create_pika_connection(config)

    while 1:
        send_metrics(channel_pika, config)
        time.sleep(config.interval)


if __name__ == "__main__":
    main()
