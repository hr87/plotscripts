import unittest
import numpy

import plotscripts.data as _data


class TestDataTest(unittest.TestCase):
    def setUp(self):
        """ setup function for tests"""
        pass

    def tearDown(self):
        """ shutdown function for tests """
        pass

    def test_column_file(self):
        data = _data.FileData()
        data.addFile('index', 'tests/data/value.test')
        data._activateDefaults()
        data._processClassData()
        index = data.index()
        index.file = 'index'
        index.column = 'second'
        values = data.getData(index)
        compare = numpy.array([5, 89, 489, 7, 984, 456, 7, 0])
        self.assertTrue((values == compare).all())

    def test_index_file(self):
        data = _data.FileData()
        data.addFile('index', 'tests/data/value2.test')
        data._activateDefaults()
        data._processClassData()
        index = data.index()
        index.file = 'index'
        index.column = 2
        values = data.getData(index)
        compare = numpy.array([5, 89, 489, 7, 984, 456, 7, 0])
        self.assertTrue((values == compare).all())


def testSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestDataTest('test_column_file'))
    suite.addTest(TestDataTest('test_index_file'))
    return suite