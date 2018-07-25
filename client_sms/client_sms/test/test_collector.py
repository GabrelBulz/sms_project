"""
    Test file for client_sms collector file
"""

import unittest
from client_sms import collector


class TestCollector(unittest.TestCase):
    """
        Test Collector class
            test - try to collect metrics that are not implemented
    """

    def test_collect_metrics(self):
        """
            Test for the case when some wrong or unimplemented metrics
            are required
        """
        non_existing_metrics = []
        non_existing_metrics.append('banane')
        test_collector = collector.Collector(77, non_existing_metrics)
        test_collector.collect_metrics()

        self.assertEqual(test_collector.metrics['banane'], 0)


if __name__ == '__main__':
    unittest.main()
