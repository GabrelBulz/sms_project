#!/usr/bin/env python
import pika
import db.ManageDB as ManageDb
import json
from threading import Thread
#from db import Model
# def initialize_DB():
ManageDb.initialize()
ManageDb.create_tables()

"""
Thread class for pika server

create a pika connection, currently set to local host
and start listen to that queue

If a pack is recived it is added to DB
"""
class threadConClientServer(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='client_server_ampq')

    def solve_queue(self,ch, method, properties, body):
        ManageDb.add_pack(json.loads(body))


    def run(self):
        self.channel.basic_consume(self.solve_queue,
                        queue='client_server_ampq',
                        no_ack=True)

        self.channel.start_consuming()

def solve_request_from_api(id_node):
    return ManageDb.get_pack(id_node)


def main():

    #create and start thread for pika connection
    threadClientSrv = threadConClientServer()
    threadClientSrv.start()

if __name__ == '__main__':
    main()
