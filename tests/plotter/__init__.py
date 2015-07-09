import unittest

# import test cases

from tests.plotter import matplotlibline as _matplotlibline
from tests.plotter import svgmap as _svgmap


def testSuite():
    plotterTests = unittest.TestSuite()
    plotterTests.addTest(_matplotlibline.testSuite())
    plotterTests.addTest(_svgmap.testSuite())
    return plotterTests
