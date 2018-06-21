#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='client_server_ampq')

def solve_queue(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(solve_queue,
                      queue='client_server_ampq',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()