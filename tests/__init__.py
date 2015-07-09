import unittest

# import test suits
import tests.plotter


def testSuite():
    plotscriptTests = unittest.TestSuite()
    plotscriptTests.addTest(tests.plotter.testSuite())
    return plotscriptTests
