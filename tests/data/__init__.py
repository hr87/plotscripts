import unittest

from tests.data import testdata as _testdata
from tests.data import methods as _methods
from tests.data import statistics as _statistics
from tests.data import filedata as _filedata


def testSuite():
    dataTest = unittest.TestSuite()
    dataTest.addTest(_testdata.testSuite())
    dataTest.addTest(_methods.testSuite())
    dataTest.addTest(_statistics.testSuite())
    dataTest.addTest(_filedata.testSuite())
    return dataTest
