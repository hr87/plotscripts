"""
Created on Jul 19, 2013

@author: Hans R Hammer
"""

import numpy
import os

from plotscripts.base.baseobject import BaseObject


class BaseTableWriter(BaseObject):
    """
    Base class for table writers
    """

    def __init__(self):
        super().__init__()

        self.input      = []    # plot data
        self.columns     = []    # columns to catch, list with column and method
        self.basedata   = None  # base data for comparison
        self.title      = None  # plot title
        self.headings   = None
        self.ndim       = 0

        self.data       = None  # storage for data

        self.defaults['rowHeadings']     = True   # headings for each row
        self.defaults['columnHeadings']  = True   # headings for each column
        self.defaults['transpose']       = True   # transpose 1d table
        self.defaults['tabledir']        = './'
        self.defaults['separator']       = '\t'

    def createTable(self):
        """
        Base method for writing tables
        """

        # init stuff
        self.out('Creating table {0}'.format(self.title))
        self.checkInput()
        self.activateDefaults()

        if self.ndim == 0:
            tableData = self.create0dTable()
        elif self.ndim == 1:
            tableData = self.create1dTable()

        # create path and filename
        path = self.options['tabledir']
        filename = self.cleanFileName('{0}'.format(self.title)) + '.tab'

        # create dir for output
        try :
            os.makedirs(path, exist_ok=True)
        except OSError as e:
            raise self.exception('Could not create directory ' + path ) from e

        # write table
        self.writeTable(path, filename, tableData)

    def create0dTable(self):
        # list for table data
        tableData = []

        # column headings
        if self.options['columnHeadings']:
            # create list
            row = []
            # empty field if row headings
            if self.options['rowHeadings']:
                row.append('Row')

            # create headings
            for column in self.columns:
                row.append(column)

        tableData.append(row)

        # loop over input keys for each row
        for idxData, datakey in enumerate(self.input):
            # create a new row
            row = []

            # set first column to headings
            if self.options['rowHeadings']:
                # either from provided list or the executioner one
                if self.headings:
                    row.append(self.headings[idxData])
                else:
                    row.append(self.data.getLegend(datakey, None))

            for column in self.columns:
                if datakey.__class__ == tuple :
                    # create copy
                    tmpDatakey = list(datakey[1])
                    # append column if necessary
                    if column[0] != None:
                        tmpDatakey.append(column[0])

                    xvalues = (self.data.getData(datakey[0], 'value', None))
                    row.append(self.data.getData(tmpDatakey, column[1], self.basedata, xvalues))
                else :
                    # create copy
                    tmpDatakey = list(datakey)
                    # append column
                    if column[0] != None:
                        tmpDatakey.append(column[0])

                    xvalues = (self.data.getXValues(tmpDatakey, 'value'))
                    row.append(self.data.getData(tmpDatakey, column[1], self.basedata, xvalues))

                    # test for right dimension
                if row[-1].ndim != 0:
                    raise self.exception('Data does not fit into table')

            # append the row to list
            tableData.append(row)

        return tableData

    def create1dTable(self):
        tableData = []
        headings = []

        for idxData, datakey in enumerate(self.input):
            for column in self.columns:
                row = []
                # get heading either from provided list or the executioner one
                if self.headings:
                    headings.append('{0}-{1}'.format(self.headings[idxData], column[1]))
                else:
                    headings.append('{0}-{1}'.format(self.data.getLegend(datakey, column), column[1]))

                if datakey.__class__ == tuple :
                    # create copy
                    tmpDatakey = list(datakey[1])
                    # append column if necessary
                    if column[0] != None:
                        tmpDatakey.append(column[0])

                    xvalues = (self.data.getData(datakey[0], 'value', None))
                    result = self.data.getData(tmpDatakey, column[1], self.basedata, xvalues)
                else :
                    # create copy
                    tmpDatakey = list(datakey)
                    # append column
                    if column[0] != None:
                        tmpDatakey.append(column[0])

                    xvalues = (self.data.getXValues(tmpDatakey, 'value'))
                    result = self.data.getData(tmpDatakey, column[1], self.basedata, xvalues)

                    # test for right dimension
                if result.ndim != 1:
                    raise self.exception('Data does not fit into table')

                row.extend(result.tolist())

                tableData.append(row)

                # transpose            
        if self.options['transpose']:
            tableData =  numpy.array(tableData).T.tolist()

        tableData = [headings] + tableData

        return tableData

    def setTitle(self, title):
        if self.title == None :
            self.title = title
        else :
            self.title = str(self.title)

    def checkInput(self):
        if self.input == [] :
            raise self.exception('No input data specified')

        # make a copy
        self.columns = list(self.columns)

        # setting column
        if self.columns == None or self.columns == []:
            self.columns = [None]

        if self.columns.__class__ != list:
            self.columns = [self.columns]

        # convert all column entries in list
        for idx, column in enumerate(self.columns):
            if column.__class__ != list:
                self.columns[idx] = [column, 'value']

        if not self.ndim in [0, 1, 2]:
            raise self.exception('Not supported dimension')

    def writeTable(self, path, filename, tableData):
        """
        Base method for writing the prepared table to a file
        """
        with open(path + '/' + filename, 'w') as tableFile:
            for row in tableData:
                tmpStr = ''
                for column in row:
                    tmpStr += '{0}\t'.format(column, self.options['separator'])

                tableFile.write(tmpStr + '\n')
