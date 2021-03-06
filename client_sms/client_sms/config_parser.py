"""
    Config Parser for client
"""

import configparser


class ConfigMachine(object):

    """ Class ConfigMachine

        constructor args -> filename as conf file

        params:
            id_node
            metrics -> as arr
            interval -> default 1

        func:
            parse_conf()
            set_filename( string type Conf file)
    """

    def __init__(self, filename):
        self.filename = filename
        self.id_node = ''
        self.metrics = []
        self.interval = 1

        self.ampq_url = ''
        self.ampq_port = ''
        self.ampq_vhost = ''
        self.ampq_user = ''
        self.ampq_password = ''

    def set_filename(self, filename):
        self.filename = filename

    def parse_conf(self):
        """
            try to parse the config file
        """

        parser = configparser.RawConfigParser()
        parser.read(self.filename)

        try:
            self.id_node = parser['CONF_MACHINE']['ID_NODE']

            # eliminate possible white spaces between metrics
            temp = parser['CONF_MACHINE']['METRICS'].split(',')
            for itr in temp:
                self.metrics.append(itr.strip())

        except Exception:
            raise Exception("missing id or metrics")

        try:
            self.interval = parser['CONF_MAHCINE']['INTERVAL']
        except Exception:
            self.interval = 1

        try:
            self.ampq_url = parser['ampq']['url']
            self.ampq_port = parser['ampq']['port']
            self.ampq_vhost = parser['ampq']['vhost']
            self.ampq_user = parser['ampq']['user']
            self.ampq_password = parser['ampq']['password']
        except Exception:
            raise Exception("missing ampq configs")
