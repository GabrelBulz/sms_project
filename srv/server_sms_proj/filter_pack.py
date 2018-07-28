"""
    This module holds a FilterPack class that will filter a list of packages
    based on required filter passed from the api

    Filter on metrics
    Filter on time interval
    New filters can be added easly
"""

import ast
import pandas


class FilterPack(object):
    """
        This class will filter a list of packages based on
        the filter request recived as an agrgumet

        Contructor pass a list of packages and a filter dict
    """

    def __init__(self, list_pack, filter_request):
        self.list_pack = list_pack
        self.filter_request = filter_request

        self.solve_filter_time_interval()
        self.solve_filter_metrics()

    def solve_filter_metrics(self):
        """
            filters the package metrics based on required metrics from api
            if metrics required are not found in package, None value
            is associated with that specific metric request
        """

        if 'metrics' in self.filter_request:
            filter_metrics = self.filter_request['metrics']
            metrics_request = {}

            temp = filter_metrics.split(',')
            for i in temp:
                metrics_request[i.strip()] = None

            for i in range(len(self.list_pack)):
                self.apply_filter_metrics(i, metrics_request.copy())


    def apply_filter_metrics(self, pack_nr, filter_metrics):
        """
            filter each package from the list
        """
        current_pack_metrics = ast.literal_eval(self.list_pack[pack_nr]['metrics'])

        for i in filter_metrics:
            if i in current_pack_metrics:
                filter_metrics[i] = current_pack_metrics[i]

        self.list_pack[pack_nr]['metrics'] = filter_metrics

    def solve_filter_time_interval(self):
        """
            create a new list of packages based on filter interval

            if filter_interval <= 0 -> will take interval = 1

            the list is created based on the interval from the first package
            first package is inserted, then it inserts the following package
            that has a timestamp >= current_time + fiter_interval
        """
        if 'interval' in self.filter_request:
            temp_list_pack = []
            temp_list_pack.append(self.list_pack[0])
            curr_time = pandas.to_datetime(self.list_pack[0]['time_stamp'])
            filter_interval = int(self.filter_request['interval'])

            if filter_interval <= 0:
                filter_interval = int(1)

            for i in self.list_pack:
                pack_time = pandas.to_datetime(i['time_stamp'])
                if (curr_time + pandas.to_timedelta(filter_interval, unit='s')) <= pack_time:
                    temp_list_pack.append(i)
                    curr_time = pandas.to_datetime(i['time_stamp'])

            self.list_pack = temp_list_pack

    def get_filtered_pack(self):
        """
            return modified list of packages
        """
        return self.list_pack
