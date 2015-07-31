""" Test to the svg map plotter
"""
import unittest
import filecmp

import plotscripts.data
import plotscripts.plotter.svg
import plotscripts.geometry.rectangular

outputPath = 'tests/plotter/'


class SvgMapTest(unittest.TestCase):
    def setUp(self):
        """ test init function """
        pass

    def tearDown(self):
        """ test shutdown function """
        pass

    def test_plotter(self):
        inputArgs = plotscripts.InputArgs()
        data = inputArgs.setData(plotscripts.data.TestData)
        plot = inputArgs.addPlot('svgmap_1', plotscripts.plotter.svg.SvgMapPlotter)
        plot.setOption('use_dirs', False)
        plot.setOption('plotdir', outputPath)
        geometry = plot.setGeometry(plotscripts.geometry.rectangular.Rectangular)
        geometry.pitch = 10
        geometry.numBlocks = [5, 5]
        mapPlot = plot.addMap('test')
        index = data.index()
        index.calcType = 'num'
        index.num = 25
        mapPlot.setIndex(index)
        inputArgs.run()  # execute
        self.assertTrue(filecmp.cmp(outputPath + 'svgmap_1_num_value_none.svg',
                                    outputPath + 'gold/svgmap_1_num_value_none.svg', False),
                        'Output files are not equal')


def testSuite():
    suite = unittest.TestSuite()
    suite.addTest(SvgMapTest('test_plotter'))
    return suite
