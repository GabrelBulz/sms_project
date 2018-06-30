#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='client_server_ampq')

channel.basic_publish(exchange='',
                      routing_key='client_server_ampq',
                      body='Mesajul trimis')

print(" [x] Sent 'Mesaj'")
connection.close()