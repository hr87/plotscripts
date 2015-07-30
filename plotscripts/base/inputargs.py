"""
Created on Apr 11, 2013

@author: Hans R Hammer

Class for running the plot scripts
"""

from plotscripts.base.baseobject import BaseObject
from plotscripts.base.exception import PlotscriptException
from plotscripts.data.basedata import BaseData
from plotscripts.plotter.baseplotter import BasePlotter
from plotscripts.table.basetablewriter import BaseTableWriter


class InputArgs(BaseObject):
    """ class for the input, can handle multiple plots at once
    provides options and run() method
    """

    def __init__(self):
        """ Constructor """
        super().__init__()
        # internal
        self._data = None        # data executioner
        self._plots = {}                # dict for defining plots
        self._tables = {}               # dict for defining tables

    def setData(self, dataClass, *args, **kwargs):
        """ set the data executioner

        :param dataClass: class of data executioner
        :param args: additional parameters
        :param kwargs: additional keyword parameters
        :return: reference to executioner
        """
        if not issubclass(dataClass, BaseData):
            self._error(dataClass.__name__ + 'is not a valid data set')
        newData = dataClass(*args, **kwargs)
        self._data = newData
        return newData

    def addPlot(self, name, plotterClass):
        """ add a plot to the input

        :param name: name of the plot
        :param plotterClass: class of the plotter
        :return: reference to new plot
        """
        if not issubclass(plotterClass, BasePlotter):
            self._error(plotterClass.__name__ + 'is not a valid plotter')
        newPlot = plotterClass(name)
        self._plots[name] = newPlot
        return newPlot

    def addTable(self, name, tableWriterClass):
        """ add a table to the input

        :param name: name of table
        :param tableWriterClass: class of table writer
        :return: reference to new table
        """
        if not issubclass(tableWriterClass, BaseTableWriter):
            self._error(tableWriterClass.__name__ + 'is not a valid table writer')
        newTable = tableWriterClass(name)
        self._tables[name] = newTable
        return newTable

    def run(self):
        """ Main method to run input, calls executioner and plotters """
        self._activateDefaults()

        # test for data
        if self._data is None:
            self._error('No data executioner found.')
            return 1

        dataName = str(self._data.__class__.__name__)

        if not issubclass(self._data.__class__, BaseData):
            self._error(dataName + 'is not a compatible data object')
            return 1

        # setting options
        self._data.copyOptions(self._options)

        # process data
        try:
            self._data.processData()
            self._retrieveOptions(self._data)
        except PlotscriptException as e:
            self._error(e)
            self._out('Could not process data with executioner ' + dataName)
            if self._options['debug']:
                raise e
            return 1

        # check for plots
        if self._plots == {} and self._tables == {}:
            self._error('No plots or tables found')
            return 1

        # loop over all plots, need to create list to delete used entries
        for plotTitle in list(self._plots.keys()):
            # get plotter name
            plotterName = str(self._plots[plotTitle].__class__.__name__)
            # test for valid plotter
            if not issubclass(self._plots[plotTitle].__class__, BasePlotter):
                self._error(plotterName + ' is not a valid plotter in plot ' + str(plotTitle))
                return 1

            try:
                # provide data
                self._plots[plotTitle].setData(self._data)
                # set option
                self._plots[plotTitle].copyOptions(self._options)
                # plot
                self._plots[plotTitle].plot()

                # clean up
                del self._plots[plotTitle]

            except PlotscriptException as e:
                self._error(e)
                self._out('Could not plot  ' + str(plotTitle))
                if self._options['debug']:
                    raise
                return 1

        # write tables
        for tableTitle in list(self._tables.keys()):
            tableWriterName = str(self._tables[tableTitle].__class__.__name__)
            # test for base class
            if not issubclass(self._tables[tableTitle].__class__, BaseTableWriter):
                self._error('{0} is not a valid table writer in table {2}'.format(tableWriterName, tableTitle))

            try:
                # provide data
                self._tables[tableTitle].setData(self._data)
                # set option
                self._tables[tableTitle].copyOptions(self._options)
                # write table
                self._tables[tableTitle].createTable()

                # clean up
                del self._tables[tableTitle]

            except PlotscriptException as e:
                self._error(e)
                self._out('Could not create table  ' + str(tableTitle))
                if self._options['debug']:
                    raise
                return 1

        self._out('Finished')
        return 0
