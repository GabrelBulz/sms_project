#!/usr/bin/env python

"""
    This module will create a pika connection to the server
    CURRENTLY THE PIKA CONNECTION IS MADE USING LOCALHOSt, but ca be modified
    to use the credentials, and port for the CONFIG param which stored parsed
    info from the conf.ini file

    A package containing the
    -id_node
    -metrics collected
    -time stamp
    will be created and send to the server based on the interval from the
    config file
"""

import ConfigParser
import datetime
import json
import sched
import time
import psutil
import pika


# schedule for repating function
SCHED = sched.scheduler(time.time, time.sleep)

CONFIG = ConfigParser.ConfigMachine('conf.ini')

CONFIG.parse_conf()

"""
int the future if i'll get a real server
the pika connection will be created using the
parameters from the config file
with config.ampq_url and so,
but until then i'll just use local host
"""
CONNECTION = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
CHANNEL = CONNECTION.channel()

CHANNEL.queue_declare(queue='client_server_ampq')


#   this function is used to get usage of every diskpart
#   but from one reason it dosen't work on my computer
#   (access denied), probably because of antivirus
def disk_usage():
    partion_usage = []

    for part in psutil.disk_partitions(all=False):
        partion_usage.append(psutil.disk_usage(part.mountpoint))

    return partition_usage


def solve_metrics(key):
    # more metrics can be added here in the future
    temp_metrics = {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'cpu_stats': psutil.cpu_stats(),
        'virtual_memory': psutil.virtual_memory(),
        'disk_usage': psutil.disk_usage('/')
        }

    try:
        result = temp_metrics.get(key, 0)
    except Exception:
        return key, 0

    return key, result


def get_metrics():
    colected_metrics = {}

    for i in CONFIG.metrics:
        key, result = solve_metrics(i)
        colected_metrics[key] = result

    return colected_metrics


# this function will create a json object to be sent to the server
# it will contain the id_node , the collected metrics, and the interval
def send_metrics(schedule):
    metrics_pack = {}
    metrics_pack['id_node'] = CONFIG.id_node
    metrics_pack['metrics'] = {}
    metrics_pack['timeStamp'] = str(datetime.datetime.now())

    temp_metrics = get_metrics()

    for i in temp_metrics.keys():
        metrics_pack['metrics'][i] = temp_metrics[i]

    CHANNEL.basic_publish(exchange='',
                          routing_key='client_server_ampq',
                          body=json.dumps(metrics_pack))

    schedule.enter(CONFIG.interval, 1, send_metrics, (schedule,))


if __name__ == "__main__":

    SCHED.enter(CONFIG.interval, 1, send_metrics, (SCHED,))
    SCHED.run()
