import unittest

# import test cases

from tests.plotter import matplotlibline as _matplotlibline

plotterSuite = unittest.TestSuite()
plotterSuite.addTest(_matplotlibline.testSuit())
