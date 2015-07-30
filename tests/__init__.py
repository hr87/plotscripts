import unittest

# import test suits
import tests.plotter
import tests.data
import tests.tablewriter


def testSuite():
    plotscriptTests = unittest.TestSuite()
    plotscriptTests.addTest(tests.data.testSuite())
    plotscriptTests.addTest(tests.plotter.testSuite())
    plotscriptTests.addTest(tests.tablewriter.testSuite())
    return plotscriptTests
