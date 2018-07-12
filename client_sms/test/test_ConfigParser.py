import sys
sys.path.append('..')
import ConfigParser
import unittest


class Test_ConfigParser(unittest.TestCase):

    def test_parse_conf(self):
        # test good config file
        config = ConfigParser.ConfigMachine('../conf.ini')
        self.assertEqual(config.parse_conf(), None)

        # test with bad filename
        config.set_filename('fail_conf.ini')
        with self.assertRaises(Exception):
            config.parse_conf()

        # test with missing ampq section
        config.set_filename('test_missing_ampq.ini')
        with self.assertRaises(Exception):
            config.parse_conf()

        # test with conf machine section
        config.set_filename('test_missing_CONF_MACHINE.ini')
        with self.assertRaises(Exception):
            config.parse_conf()


if __name__ == 'main':
    unittest.main()
