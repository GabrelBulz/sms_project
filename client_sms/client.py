#!/usr/bin/env python

"""
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

import ConfigParser
import datetime
import json
import sched
import time
import psutil
import pika


# schedule for repeating function send_metrics
SCHED = sched.scheduler(time.time, time.sleep)

CONFIG = ConfigParser.ConfigMachine('conf.ini')

CONFIG.parse_conf()

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

CONNECTION = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
CHANNEL = CONNECTION.channel()

CHANNEL.queue_declare(queue='client_server_ampq')


def disk_usage():
    """
        this function is used to get usage of every diskpart
        but from one reason it dosen't work on my computer
        (access denied), probably because of antivirus
    """
    partion_usage = []

    for part in psutil.disk_partitions(all=False):
        partion_usage.append(psutil.disk_usage(part.mountpoint))

    return partition_usage


def solve_metrics(key):
    """
        based on the key it returns the metrics collected with psutil
        more metrics can be added here in the future
    """
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


def send_metrics(schedule):
    """
        this function will create a json object to be sent to the server
        it will contain the id_node , the collected metrics, and the interval
    """
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

    # recall function at setted interval (in sec)
    schedule.enter(int(CONFIG.interval), 1, send_metrics, (schedule,))


def main():
    SCHED.enter(CONFIG.interval, 1, send_metrics, (SCHED,))
    SCHED.run()


if __name__ == "__main__":
    main()
