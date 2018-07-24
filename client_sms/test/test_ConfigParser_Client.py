import sys
import unittest
sys.path.append('..')
import config_parser
import client


class Test_ConfigParser(unittest.TestCase):

    def test_parse_conf(self):

        # test good config file
        config = config_parser.ConfigMachine('../conf.ini')
        self.assertEqual(config.parse_conf(), None)

        # test with bad filename
        config.set_filename('fail_conf.ini')
        with self.assertRaises(Exception):
            config.parse_conf()

    def test_parse_conf_missing_ampq_section(self):
        # test with missing ampq section
        config = config_parser.ConfigMachine('test_missing_ampq')
        with self.assertRaises(Exception):
            config.parse_conf()

    def test_parse_conf_missing_conf_machine_section(self):
        # test with conf machine section
        config = config_parser.ConfigMachine('test_missing_CONF_MACHINE')
        with self.assertRaises(Exception):
            config.parse_conf()

    def test_Client_solve_metrics(self):
        """
            Test for the case when some wrong or unimplemented metrics
            are required
        """
        non_existing_key = 'banane'

        self.assertEqual(client.solve_metrics(non_existing_key), ('banane', 0))


if __name__ == 'main':
    unittest.main()
