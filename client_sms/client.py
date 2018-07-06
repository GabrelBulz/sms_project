#!/usr/bin/env python
import pika
import ConfigParser
import psutil
import json
import sched
import time
import datetime


# schedule for repating function
Sched = sched.scheduler(time.time, time.sleep)

config = ConfigParser.ConfigMachine('conf.ini')

config.parse_conf()

"""
int the future if i'll get a real server
the pika connection will be created using the
parameters from the config file
with config.ampq_url and so,
but until then i'll just use local host
"""
connection = pika.BlockingConnection(pika.ConnectionParameters(
                                                            host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='client_server_ampq')


#   this function is used to get usage of every diskpart
#   but from one reason it dosen't work on my computer
#   (access denied), probably because of antivirus
def disk_usage():
    partion_usage = []

    for part in psutil.disk_partitions(all=False):
        partion_usage.append(psutil.disk_usage(part.mountpoint))

    return partition_usage


def solve_metrics(key):
    temp_metrics = {
                        'cpu_percent': psutil.cpu_percent(interval=1),
                        'cpu_stats': psutil.cpu_stats(),
                        'virtual_memory': psutil.virtual_memory(),
                        'disk_usage': psutil.disk_usage('/')
                    }

    try:
        result = temp_metrics.get(key, 0)
    except Exception as e:
        return key, 0

    return key, result


def get_metrics():
    colected_metrics = {}

    for i in config.metrics:
        key, result = solve_metrics(i)
        colected_metrics[key] = result

    return colected_metrics


# this function will create a json object to be sent to the server
# it will contain the id_node , the collected metrics, and the interval
def send_metrics(schedule):
    metrics_pack = {}
    metrics_pack['id_node'] = config.id_node
    metrics_pack['metrics'] = {}
    metrics_pack['timeStamp'] = str(datetime.datetime.now())

    temp_metrics = get_metrics()

    for i in temp_metrics.keys():
        metrics_pack['metrics'][i] = temp_metrics[i]

    channel.basic_publish(exchange='',
                          routing_key='client_server_ampq',
                          body=json.dumps(metrics_pack))

    schedule.enter(config.interval, 1, send_metrics, (schedule,))


if __name__ == "__main__":

    Sched.enter(config.interval, 1, send_metrics, (Sched,))
    Sched.run()
