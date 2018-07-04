#!/usr/bin/env python
import pika



# ##client -> server
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()


# channel.queue_declare(queue='client_server_ampq')

# def solve_queue(ch, method, properties, body):
#     print(" [x] Received %r" % body)

# channel.basic_consume(solve_queue,
#                       queue='client_server_ampq',
#                       no_ack=True)

# channel.start_consuming()




## api -> server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def on_request(ch, method, props, body):
    print(body)

    response = "ok"

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

channel.start_consuming()


