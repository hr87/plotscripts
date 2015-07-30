""" Test module for base data methods
"""

import unittest
import numpy

import plotscripts.data as _data


class MethodTest(unittest.TestCase):
    def setUp(self):
        """ setup function for tests"""
        self.data = _data.TestData()
        self.data._checkInput()
        self.data.processData()

        self.index = self.data.index()
        self.index.calcType = 'num'
        self.index.num = 2
        self.index.min = 2
        self.index.step = 1

        self.base = self.data.index()
        self.base.calcType = 'num'
        self.base.num = 2
        self.base.min = 1
        self.base.step = 1

    def tearDown(self):
        """ shutdown function for tests """
        pass

    def test_value(self):
        self.index.method = self.data.Methods.value
        self.assertTrue((self.data.getData(self.index, self.base)
                         == numpy.array([2, 3])).all())

    def test_difference(self):
        self.index.method = self.data.Methods.difference
        print(self.data.getData(self.index, self.base))
        self.assertTrue((self.data.getData(self.index, self.base)
                         == numpy.array([1, 1])).all())

    def test_deviation(self):
        self.index.method = self.data.Methods.deviation
        print(self.data.getData(self.index, self.base))
        self.assertTrue((self.data.getData(self.index, self.base)
                         == numpy.array([100, 50])).all())

    def test_norm_max(self):
        self.data.setOption('normalize', 'max')
        self.index.method = self.data.Methods.normalized
        print(self.data.getData(self.index, self.base))
        self.assertTrue((self.data.getData(self.index, self.base)
                         == numpy.array([2.0/3.0, 3.0/3.0])).all())

    def test_norm_sum(self):
        self.data.setOption('normalize', 'sum')
        self.index.method = self.data.Methods.normalized
        print(self.data.getData(self.index, self.base))
        self.assertTrue((self.data.getData(self.index, self.base)
                         == numpy.array([2.0/5.0, 3.0/5.0])).all())

    def test_norm_avg(self):
        self.data.setOption('normalize', 'avg')
        self.index.method = self.data.Methods.normalized
        print(self.data.getData(self.index, self.base))
        self.assertTrue((self.data.getData(self.index, self.base)
                         == numpy.array([2.0/2.5, 3.0/2.5])).all())


def testSuite():
    suite = unittest.TestSuite()
    suite.addTest(MethodTest('test_value'))
    suite.addTest(MethodTest('test_difference'))
    suite.addTest(MethodTest('test_deviation'))
    suite.addTest(MethodTest('test_norm_max'))
    suite.addTest(MethodTest('test_norm_sum'))
    suite.addTest(MethodTest('test_norm_avg'))
    return suite
