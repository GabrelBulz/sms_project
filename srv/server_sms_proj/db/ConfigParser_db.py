import configparser


class ConfigMachine_db(object):

    """ Class ConfigMachine

        constructor args -> filename as conf file

        params:
            url

        func:
            parse_conf()
            set_filename( string type Conf file)
    """

    def __init__(self, filename):
        self.filename = filename
        self.url = 'sqlite:///:memory:'

    def set_filename(self, filename):
        self.filename = filename

    def parse_conf(self):

        parser = configparser.RawConfigParser()
        parser.read(self.filename)

        try:
            self.url = str(parser['db']['url'])
        except Exception:
            print("missing db url")
