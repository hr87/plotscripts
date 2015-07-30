import unittest
import numpy

import plotscripts.data as _data


class StatisticTest(unittest.TestCase):
    def setUp(self):
        """ setup function for tests"""
        self.data = _data.TestData()
        stat = self.data.addStatistic('test')
        for idx in range(100):
            index = self.data.index()
            index.calcType = 'num'
            index.num = 2
            index.min = idx
            index.step = idx + 1
            stat.addInput(index)
        stat.columns = ['column']
        self.data._checkInput()
        self.data.processData()

    def tearDown(self):
        """ shutdown function for tests """
        pass

    def test_avg(self):
        index = self.data.statisticIndex()
        index.name = 'test'
        index.field = _data.StatisticData.Fields.avg
        index.column = 'column'
        self.assertTrue((self.data.getData(index)
                        == numpy.array([49.5, 100.0])).all())

    def test_min(self):
        index = self.data.statisticIndex()
        index.name = 'test'
        index.field = _data.StatisticData.Fields.min
        index.column = 'column'
        self.assertTrue((self.data.getData(index)
                        == numpy.array([0.0, 1.0])).all())

    def test_max(self):
        index = self.data.statisticIndex()
        index.name = 'test'
        index.field = _data.StatisticData.Fields.max
        index.column = 'column'
        self.assertTrue((self.data.getData(index)
                        == numpy.array([99.0, 199.0])).all())


def testSuite():
    suite = unittest.TestSuite()
    suite.addTest(StatisticTest('test_avg'))
    suite.addTest(StatisticTest('test_min'))
    suite.addTest(StatisticTest('test_max'))
    return suite
