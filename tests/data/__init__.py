import unittest

from tests.data import testdata as _testdata
from tests.data import statistics as _statistics


def testSuite():
    dataTest = unittest.TestSuite()
    dataTest.addTest(_testdata.testSuite())
    dataTest.addTest(_statistics.testSuite())
    return dataTest
