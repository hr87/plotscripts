""" Test to the matplotlib line plotter
"""
import unittest
import filecmp

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
        data = inputArgs.setData(plotscripts.data.TestData)
        plot = inputArgs.addPlot('matplotlib_1', plotscripts.plotter.matplotlib.LinePlotter)
        plot.setOption('use_dirs', False)               # do not generate folder structure
        plot.setOption('plotdir', outputPath)           # set folder to test folder
        plot.setOption('format', 'png')                 # output format to png, svg gives problems with comparison
        line = plot.addLine('line')                     # add a line
        index = data.index()
        index.calcType = 'num'
        index.num = 10
        line.setIndex((index, index))                    # setting x and y values
        line.color = line.ColorList.red                 # set line color
        line.lineStyle = line.LineStyleList.dashed      # set line style
        line.markerStyle = line.MarkerStyleList.dot     # set marker style
        line.markerSize = 1.1                           # set marker size
        inputArgs.run()                                 # execute
        self.assertTrue(filecmp.cmp(outputPath + 'matplotlib_1_value_none.png',
                                    outputPath + 'gold/matplotlib_1_value_none.png', False),
                        'Output files are not equal')


def testSuite():
    suite = unittest.TestSuite()
    suite.addTest(_MatplotlibLineTest('test_plotter'))
    return suite
