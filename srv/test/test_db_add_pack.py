import datetime
import unittest
import sys
sys.path.append('..')
import server


class Test_db_add_pack(unittest.TestCase):

    def create_good_pack(self):
        pack = {}

        pack['id_node'] = int(599)
        pack['metrics'] = {}
        pack['timeStamp'] = str(datetime.datetime.now())

        return pack

    def create_bad_pack(self):
        pack = {}

        pack['id_node'] = 'test_id'
        pack['metrics'] = 2
        pack['timeStamp'] = 2.9

        return pack

    def test_add_pack_good(self):
        """
            Test adding a good package format to the db
        """
        good_pack = self.create_good_pack()

        self.assertEqual(server.manageDb.add_pack(good_pack), None)

    def test_add_pack_bad(self):
        """
            Test adding a bad package format to the db
        """
        bad_pack = self.create_bad_pack()
        with self.assertRaises(Exception):
            server.manageDb.add_pack(bad_pack)


if __name__ == '__main__':
    unittest.main()
