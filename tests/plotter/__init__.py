import unittest

# import test cases

from tests.plotter import matplotlibline as _matplotlibline
from tests.plotter import svgmap as _svgmap

plotterSuite = unittest.TestSuite()
plotterSuite.addTest(_matplotlibline.testSuit())
plotterSuite.addTest(_svgmap.testSuit())
