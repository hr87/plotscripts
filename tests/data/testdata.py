import unittest
import numpy

import plotscripts.data as _data


class TestDataTest(unittest.TestCase):
    def setUp(self):
        """ setup function for tests"""
        self.data = _data.TestData()
        self.data.processData()

    def tearDown(self):
        """ shutdown function for tests """
        pass

    def test_index_data(self):
        index = self.data.index()
        index.calcType = 'num'
        index.num = 10
        index.min = 0
        index.step = 1
        values = self.data.getData(index)
        self.assertTrue((values == numpy.arange(10)).all())

    def test_random_data(self):
        index = self.data.index()
        index.calcType = 'rnd'
        index.num = 10
        index.min = 0
        index.max = 1
        values = self.data.getData(index)
        self.assertEqual(len(values), 10)


def testSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestDataTest('test_index_data'))
    suite.addTest(TestDataTest('test_random_data'))
    return suite
