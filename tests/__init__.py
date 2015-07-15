import unittest

# import test suits
import tests.plotter
import tests.data


def testSuite():
    plotscriptTests = unittest.TestSuite()
    plotscriptTests.addTest(tests.data.testSuite())
    plotscriptTests.addTest(tests.plotter.testSuite())
    return plotscriptTests
