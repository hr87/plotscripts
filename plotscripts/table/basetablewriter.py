"""
Created on Jul 19, 2013

@author: Hans R Hammer
"""

import numpy
import os
import copy

from plotscripts.base.baseobject import BaseObject
from plotscripts.data.basedata import BaseData


class BaseTableWriter(BaseObject):
    """
    Base class for table writers
    """

    class Row(BaseObject):
        """ class for one column
        """

        def __init__(self, name):
            """ Constructor
            :param name: column name
            :return: None
            """
            super().__init__()

            # internal
            self._name = name
            self._data = None

        def setIndex(self, index):
            """ set the index
            """
            if not (isinstance(index, BaseData.Index) or isinstance(index, tuple)):
                raise self._exception('Invalid index object "{0}"'.format(index))
            self._data = copy.deepcopy(index)

    def __init__(self, name):
        super().__init__()

        self.columns = [None]  # columns to catch
        self.methods = [None]
        self.title = name  # plot title
        self.ndim = 0

        # internal
        self._data = None  # storage for data
        self._rows = []     # table rows
        self._basedata = None  # base data for comparison
        self._name = name

        # add options
        self._addDefault('rowHeadings', True, 'headings for each row', 'local')
        self._addDefault('columnHeadings', True, 'headings for each column')
        self._addDefault('transpose', True, 'transpose 1d table', 'local')
        self._addDefault('tabledir', './', 'folder for tables', 'local')
        self._addDefault('separator', '\t', 'table separator', 'local')

    def setData(self, data):
        """ Set data set
        :param data: data set
        :return: None
        """
        self._data = data

    def setBaseIndex(self, index):
        """ Set the index for the base data
        :param index: index object
        :return: None
        """
        if not isinstance(index, BaseData.Index):
            raise self._exception('Invalid index object "{0}"'.format(index))
        self._basedata = copy.deepcopy(index)

    def addRow(self, name):
        """ Add a row to the table
        """
        row = self.Row(name)
        self._rows.append(row)
        return row

    def createTable(self):
        """
        Base method for writing tables
        """

        # init stuff
        self._out('Creating table {0}'.format(self.title))
        self._checkInput()
        self._activateDefaults()

        # TODO automatically
        if self.ndim == 0:
            tableData = self.create0dTable()
        elif self.ndim == 1:
            tableData = self.create1dTable()
        else:
            raise self._exception('Number of dimensions to high')

        # create path and filename
        path = self._getOption('tabledir')
        filename = self._cleanFileName('{0}'.format(self._name))

        # create dir for output
        try:
            os.makedirs(path, exist_ok=True)
        except OSError as e:
            raise self._exception('Could not create directory ' + path) from e

        # write table
        self.writeTable(path, filename, tableData)

    def create0dTable(self):
        # list for table data
        tableData = []

        # column headings
        if self._getOption('columnHeadings'):
            # create list
            row = []
            # empty field if row headings
            if self._getOption('rowHeadings'):
                row.append('Row')

            # create headings
            for column in self.columns:
                for method in self.methods:
                    row.append('{0}/{1}'.format(column, method))

            tableData.append(row)

        # loop over input keys for each row
        for rowInput in self._rows:
            # create a new row
            row = []
            datakey = rowInput._data

            # set first column to headings
            if self._getOption('rowHeadings'):
                row.append(rowInput._name)

            for column in self.columns:
                # adjust base data column
                if column is not None:
                    if isinstance(self._basedata, tuple):
                        self._basedata[1].column = column
                    else:
                        self._basedata.column = column

                for method in self.methods:
                    if isinstance(datakey, tuple):
                        # create copy
                        # append column if necessary
                        if column[0] is not None:
                            datakey[1].column = column[0]
                        if method is not None:
                            datakey[1].method = method

                        xvalues = (self._data.getData(datakey[0]))
                        row.append(self._data.getData(datakey[1], self._basedata, xvalues))
                    else:
                        # append column
                        if column is not None:
                            datakey.column = column
                        if method is not None:
                            datakey.method = method

                        xvalues = (self._data.getXValues(datakey))
                        row.append(self._data.getData(datakey, self._basedata, xvalues))

                        # test for right dimension
                    if row[-1].ndim != 0:
                        raise self._exception('Data does not fit into table')

            # append the row to list
            tableData.append(row)

        return tableData

    def create1dTable(self):
        tableData = []
        headings = []

        for rowInput in self._rows:
            for column in self.columns:
                for method in self.methods:
                    row = []
                    datakey = rowInput._data
                    # get heading either from provided list or the executioner one
                    headings.append('{0}-{1}/{2}'.format(rowInput._name, column, method))

                    if isinstance(datakey, tuple):
                        # append column if necessary
                        if column is not None:
                            datakey[1].column = column
                        if method is not None:
                            datakey[1].method = method

                        xvalues = (self._data.getData(datakey[0]))
                        result = self._data.getData(datakey[1], self._basedata, xvalues)
                    else:
                        # append column
                        if column is not None:
                            datakey.column = column
                        if method is not None:
                            datakey.method = method

                        xvalues = (self._data.getXValues(datakey))
                        result = self._data.getData(datakey, self._basedata, xvalues)

                        # test for right dimension
                    if result.ndim != 1:
                        raise self._exception('Data does not fit into table')

                    row.extend(result.tolist())

                    tableData.append(row)

                # transpose            
        if self._getOption('transpose'):
            tableData = numpy.array(tableData).T.tolist()

        tableData = [headings] + tableData

        return tableData

    def setTitle(self, title):
        if self.title is None:
            self.title = title
        else:
            self.title = str(self.title)

    def _checkInput(self):
        if self._rows is []:
            raise self._exception('No input data specified')

        # make a copy
        self.columns = list(self.columns)

        # setting column
        if self.columns is None or self.columns == []:
            self.columns = [None]

        if self.columns.__class__ != list:
            self.columns = [self.columns]

        if self.ndim not in [0, 1]:
            raise self._exception('Not supported dimension')

    def writeTable(self, path, filename, tableData):
        """
        Base method for writing the prepared table to a file
        """
        raise self._exception('Not implemented in base class')
