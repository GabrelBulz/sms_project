import configparser


class ConfigMachineSRV(object):

	def __init__(self, filename):
        self.ampq_url = ''
        self.ampq_port = ''
        self.ampq_vhost = ''
        self.ampq_user = ''
        self.ampq_password = ''

	def set_filename(self, filename):
		self.filename = filename

	def parse_conf(self):

		parser = configparser.RawConfigParser()
		parser.read(self.filename)

        try:
            self.ampq_url = parser['ampq']['url']
            self.ampq_port = parser['ampq']['port']
            self.ampq_vhost = parser['ampq']['vhost']
            self.ampq_user = parser['ampq']['user']
            self.ampq_password = parser['ampq']['password']
        except Exception:
            print("missing ampq configs")
