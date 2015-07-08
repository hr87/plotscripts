""" Test to the matplotlib line plotter
"""
import unittest
import filecmp

import plotscripts.base.exception
import plotscripts.data
import plotscripts.plotter.matplotlib

outputPath = 'tests/plotter/'

class _MatplotlibLineTest(unittest.TestCase):
    def setUp(self):
        """ test init function """
        pass

    def tearDown(self):
        """ test shutdown function """
        pass

    def test_plotter(self):
        inputArgs = plotscripts.InputArgs()
        inputArgs.setData(plotscripts.data.TestData)
        plot = inputArgs.addPlot('matplotlib_1', plotscripts.plotter.matplotlib.LinePlotter)
        plot.setOption('use_dirs', False)
        plot.setOption('plotdir', outputPath)
        line = plot.addLine()                           # add a line
        line.data = (['num', 10], ['num', 10])          # setting x and y values
        line.color = line.ColorList.red                 # set line color
        line.lineStyle = line.LineStyleList.dashed      # set line style
        line.markerStyle = line.MarkerStyleList.dot     # set marker style
        line.markerSize = 1.1                           # set marker size
        inputArgs.run()                                 # execute
        # self.assertTrue(filecmp.cmp(outputPath + 'matplotlib_1_value_none.svg',
        #                             outputPath + 'gold/matplotlib_1_value_none.svg', False),
        #                 'Output files are not equal')


def testSuit():
    suite = unittest.TestSuite()
    suite.addTest(_MatplotlibLineTest('test_plotter'))
    return suite
