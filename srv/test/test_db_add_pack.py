import unittest
import datetime
import json
import pika
import sys
sys.path.append('..')
import server


class Test_db_add_pack():

    def __init__(self):
        print('init')

    def create_good_pack(self):
        pack = {}

        pack['id'] = 599
        pack['metrics'] = 'some random metrics'
        pack['timeStamp'] = str(datetime.datetime.now())

        return pack


    def create_bad_pack(self):
        pack = {}

        pack['id'] = 'test_id'
        pack['metrics'] = 2
        pack['timeStamp'] = 2.9

        return pack

    def test_add_pack(self):
        """
            Test adding a good and a bad package format to the db
        """

        # connection = pika.BlockingConnection(pika.ConnectionParameters(
        #     host='localhost'))
        # channel = connection.channel()

        # channel.queue_declare(queue='client_server_ampq')

        # channel.basic_publish(exchange='',
        #                       routing_key='client_server_ampq',
        #                       body=json.dumps(metrics_pack))

        good_pack = self.create_good_pack()

        print(server.ManageDb.add_pack(json.dumps(good_pack)))


if __name__ == '__main__':
    t= Test_db_add_pack()
    t.test_add_pack()

