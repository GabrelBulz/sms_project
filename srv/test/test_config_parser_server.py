import sys
import unittest
sys.path.append('..')
import config_parser_server


class TestConfigParserSERVER(unittest.TestCase):

    def test_parse_conf(self):

        # test good config file
        config = config_parser_server.ConfigMachineSRV('../default_conf.ini')
        self.assertEqual(config.parse_conf(), None)

        # test with bad filename
        config.set_filename('fail_conf.ini')
        with self.assertRaises(Exception):
            config.parse_conf()

    def test_parse_conf_missing_ampq_section(self):
        # test with missing ampq section
        config = config_parser_server.ConfigMachineSRV('test_missing_ampq')
        with self.assertRaises(Exception):
            config.parse_conf()


if __name__ == 'main':
    unittest.main()
