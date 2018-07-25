"""
    An object for collecting all the metrics, specified
    as a list, in constrctor
"""

import datetime
import json
import psutil


class Collector(object):
    """
        Collector for metrics

        constructor agrs:
            id_node default
            a list of metrics to be collected
    """

    def __init__(self, id_node, metrics_to_collect):
        self.id_node = id_node
        self.time_stamp = datetime.datetime.now()
        self.metrics_to_collect = metrics_to_collect
        self.metrics = {}

    def collect_metrics(self):
        """
            collect each metric separately and
            return a dict with colllected metrics
        """
        temp_metrics = {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'cpu_stats': psutil.cpu_stats(),
            'virtual_memory': psutil.virtual_memory(),
            'disk_usage': psutil.disk_usage('/')
            }

        for key in self.metrics_to_collect:
            try:
                result = temp_metrics.get(key, 0)
            except KeyError:
                result = 0
            self.metrics[key] = result

    def to_dict(self):
        """
            return a pack as dict
        """
        pack = {}

        pack['id_node'] = int(self.id_node)
        pack['metrics'] = self.metrics
        pack['time_stamp'] = str(self.time_stamp)

        return pack

    def to_json(self):
        """
            create the package as a dict,
            and return that package jsonifyed
        """
        return json.dumps(self.to_dict())
