"""
    Test client config parser
"""

import sys
import unittest
sys.path.append('..')
import config_parser


class TestConfigParser(unittest.TestCase):
    """
        Test for client config parse
            Test for bad file name
            Test for missing ampq section
            Test for missing metrics for machine
    """

    def test_parse_conf(self):
        """
            test good config file
        """
        config = config_parser.ConfigMachine('../default_conf.ini')
        self.assertEqual(config.parse_conf(), None)

        # test with bad filename
        config.set_filename('fail_conf.ini')
        with self.assertRaises(Exception):
            config.parse_conf()

    def test_parse_conf_missing_ampq_section(self):
        """
            test with missing ampq section
        """
        config = config_parser.ConfigMachine('test_missing_ampq')
        with self.assertRaises(Exception):
            config.parse_conf()

    def test_parse_conf_missing_conf_machine_section(self):
        """
            test with conf machine section
        """
        config = config_parser.ConfigMachine('test_missing_CONF_MACHINE')
        with self.assertRaises(Exception):
            config.parse_conf()


if __name__ == 'main':
    unittest.main()
