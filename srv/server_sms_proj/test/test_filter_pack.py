"""
    Test filter module
"""

import unittest
from server_sms_proj import filter_pack

class TestFilter(unittest.TestCase):
    """
        create a test for filter module
        Test for require an invalid metric
        Test for a non numerical required_interval
    """

    def create_package(self):
        """
            create a valid package for test
        """
        package = {}

        package['id'] = 999
        package['metrics'] = "{'cpu_percent' : 10}"
        package['time_stamp'] = "2018-07-25 14:45:48.656737"

        return package

    def test_not_existing_metrics(self):
        """
            Test for non existing metric
            Result should be None
        """
        list_pack = []
        list_pack.append(self.create_package())

        filter_req = {}
        filter_req['metrics'] = "non_existing_metrics"

        filt = filter_pack.FilterPack(list_pack, filter_req)

        res = filt.get_filtered_pack()
        self.assertEqual(res[0]['metrics']['non_existing_metrics'], None)

    def test_bad_interval(self):
        """
            Test for non numerical required_interval
            An error should be raise
        """
        list_pack = []
        list_pack.append(self.create_package())

        filter_req = {}
        filter_req['interval'] = 'ana'

        with self.assertRaises(ValueError):
            filter_pack.FilterPack(list_pack, filter_req)


if __name__ == '__main__':
    unittest.main()
