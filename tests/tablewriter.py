""" Table writer test file
"""

import unittest
import filecmp
import plotscripts.data
import plotscripts.table

outputPath = 'tests/tables/'


class TxtTableTest(unittest.TestCase):
    def setUp(self):
        """ test init function """
        pass

    def tearDown(self):
        """ test shutdown function """
        pass

    def test_0d_data(self):
        inputArg = plotscripts.InputArgs()
        inputArg.setOption('debug', True)
        inputArg.setOption('tabledir', outputPath)
        inputArg.setData(plotscripts.data.TestData)

        index = plotscripts.data.TestData.index()
        index.calcType = 'num'
        index.num = 1
        index.min = 0

        table = inputArg.addTable('test', plotscripts.table.TxtTableWriter)
        table.title = 'Test Table'

        row = table.addRow('first row')
        row.setIndex(index)

        index.min = 2
        row = table.addRow('My 2nd')
        row.setIndex(index)
        inputArg.run()
        self.assertTrue(filecmp.cmp(outputPath + 'test.tab',
                                    outputPath + 'gold/test.tab', False),
                        'Output files are not equal')

    def test_1d_data(self):
        inputArg = plotscripts.InputArgs()
        inputArg.setOption('debug', True)
        inputArg.setOption('tabledir', outputPath)
        inputArg.setData(plotscripts.data.TestData)

        table = inputArg.addTable('test_big', plotscripts.table.TxtTableWriter)
        table.title = 'Big test table'
        table.ndim = 1  # can handle big data

        index = plotscripts.data.TestData.index()
        index.calcType = 'num'
        index.num = 10
        index.min = 0
        index.step = 1

        row = table.addRow('First')
        row.setIndex(index)

        index.step = 2
        row = table.addRow('Second')
        row.setIndex(index)

        # run input
        inputArg.run()
        self.assertTrue(filecmp.cmp(outputPath + 'test_big.tab',
                                    outputPath + 'gold/test_big.tab', False),
                        'Output files are not equal')


class LatexTableTest(unittest.TestCase):
    def setUp(self):
        """ test init function """
        pass

    def tearDown(self):
        """ test shutdown function """
        pass

    def test_0d_data(self):
        inputArg = plotscripts.InputArgs()
        inputArg.setOption('debug', True)
        inputArg.setOption('tabledir', outputPath)
        inputArg.setData(plotscripts.data.TestData)

        index = plotscripts.data.TestData.index()
        index.calcType = 'num'
        index.num = 1
        index.min = 0

        table = inputArg.addTable('test', plotscripts.table.LatexTableWriter)
        table.title = 'Test Table'

        row = table.addRow('first row')
        row.setIndex(index)

        index.min = 2
        row = table.addRow('My 2nd')
        row.setIndex(index)
        inputArg.run()
        self.assertTrue(filecmp.cmp(outputPath + 'test.tex',
                                    outputPath + 'gold/test.tex', False),
                        'Output files are not equal')

    def test_1d_data(self):
        inputArg = plotscripts.InputArgs()
        inputArg.setOption('debug', True)
        inputArg.setOption('tabledir', outputPath)
        inputArg.setData(plotscripts.data.TestData)

        table = inputArg.addTable('test_big', plotscripts.table.LatexTableWriter)
        table.title = 'Big test table'
        table.ndim = 1  # can handle big data

        index = plotscripts.data.TestData.index()
        index.calcType = 'num'
        index.num = 10
        index.min = 0
        index.step = 1

        row = table.addRow('First')
        row.setIndex(index)

        index.step = 2
        row = table.addRow('Second')
        row.setIndex(index)

        # run input
        inputArg.run()
        self.assertTrue(filecmp.cmp(outputPath + 'test_big.tex',
                                    outputPath + 'gold/test_big.tex', False),
                        'Output files are not equal')


def testSuite():
    suite = unittest.TestSuite()
    suite.addTest(TxtTableTest('test_0d_data'))
    suite.addTest(TxtTableTest('test_1d_data'))

    suite.addTest(LatexTableTest('test_0d_data'))
    suite.addTest(LatexTableTest('test_1d_data'))
    return suite
