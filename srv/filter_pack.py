import json

class FilterPack(object):

    def __init__(self, list_pack, filter_request):
        self.list_pack = list_pack
        self.filter_request = filter_request
        self.metrics_request = {}

        self.solve_filter_metrics()

    def solve_filter_metrics(self):

        if 'metrics' in self.filter_request:
            filter_metrics = self.filter_request['metrics']

            temp = filter_metrics.split(',')
            for i in temp:
                self.metrics_request[i.strip()] = None

            for i in range(len(self.list_pack)):
                self.apply_filter_metrics(i, self.metrics_request)

            print(self.list_pack)

    def apply_filter_metrics(self, pack_nr, filter_metrics):
        temp_metrics = filter_metrics

        for i in filter_metrics:
            if i in (self.list_pack[pack_nr])['metrics']:
                td = json.dump(self.list_pack[pack_nr]['metrics'].replace("'",'"'))
                print(td)
                # temp_metrics[i] = (self.list_pack[pack_nr])['metrics'][i]

        self.list_pack[pack_nr]['metrics'] = temp_metrics
