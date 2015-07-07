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

    :var data: Executioner for data processing, must be a subclass of BaseValue
    :var plot: dict of plots, keyword is plot title if not otherwise given
    :var table: dict of tables to create
    """

    def __init__(self):
        """
        Constructor
        """

        super().__init__()
        self.data = None      # data executioner
        self.plot = {}        # dict for defining plots
        self.table = {}       # dict for defining tables

    def run(self) :
        """
        method to run input, calls executioner and plotters
        """

        self.activateDefaults()

        # test for data
        if self.data is None :
            self.error('No data executioner found.')
            return 1

        executioner = str(self.data.__class__.__name__)

        if not issubclass(self.data.__class__, BaseData) :
            self.error(executioner +  'is not a compatible data executioner')
            return 1

        # setting options
        self.data.setOptions(self.options)

        # process data
        try :
            self.data.processData()
            self.getOptions(self.data)
        except PlotscriptException as e :
            self.error(e)
            self.out('Could not process data with executioner ' + executioner)
            if self.options['debug']:
                raise e
            return 1

        # check for plots
        if self.plot == {} and self.table == {} :
            self.error('No plots or tables found')
            return 1

        # loop over all plots, need to create list to delete used entries
        for plotTitle in list(self.plot.keys()) :
            # get plotter name
            plotterName = str(self.plot[plotTitle].__class__.__name__)
            # test for valid plotter
            if not issubclass(self.plot[plotTitle].__class__, BasePlotter) :
                self.error(plotterName + ' is not a valid plotter in plot ' + str(plotTitle) )
                return 1

            try :
                # set plot title
                self.plot[plotTitle].setTitle(plotTitle)
                # provide data
                self.plot[plotTitle].data = self.data
                # set option
                self.plot[plotTitle].setOptions(self.options)
                # plot
                self.plot[plotTitle].plot()

                # clean up
                del self.plot[plotTitle]

            except PlotscriptException as e :
                self.error(e)
                self.out('Could not plot  ' + str(plotTitle) )
                if self.options['debug']:
                    raise
                return 1

        # write tables
        for tableTitle in list(self.table.keys()):
            tableWriterName = str(self.table[tableTitle].__class__.__name__)
            # test for base class
            if not issubclass(self.table[tableTitle].__class__, BaseTableWriter):
                self.error('{0} is not a valid table writter in table {2}'.format(tableWriterName, tableTitle))

            try:
                # set plot title
                self.table[tableTitle].setTitle(tableTitle)
                # provide data
                self.table[tableTitle].data = self.data
                # set option
                self.table[tableTitle].setOptions(self.options)
                # write table
                self.table[tableTitle].createTable()

                # clean up
                del self.table[tableTitle]

            except PlotscriptException as e:
                self.error(e)
                self.out('Could not create table  ' + str(tableTitle) )
                if self.options['debug']:
                    raise
                return 1

        self.out('Finished')
        return 0
