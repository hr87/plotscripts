"""
Created on Apr 10, 2013

@author: Hans R Hammer

Executioner for column sorted data
"""

import numpy
from plotscripts.data.basedata import BaseData



class ColumnData(BaseData):
    """
    Executioner for column sorted data
    @see BaseValue
    @keyword headings: option Turns on/off headings in input files, default = None, only when first row is not convertable
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()

        self.file       = {}                   # file names
        self._addDefault('dir', '.', 'folder to look for files', 'private')
        self._addDefault('headings', None, 'Cannot remember', 'private')

    def processClassData(self):
        """
        read and process all the data,
        overwrites base method
        """
        # read input files
        self.readFiles()

    def getClassData(self, index):
        """
        base interface method for plotter to get data, returns the corresponding data for file index, column index
        methods available are: value, rel, diff
        index: file, column
        :param index: list with index of data
        :param meth: method for data processing, default = value
        :param base: list with index for base data needed for some methods, default = None
        :param x: x values for some methods, may be changed, default = None
        :return: numpy array with data
        """
        try:
            filekey = index[0]
            column = index[1]
        except IndexError as e:
            raise self._exception('Wrong index: ' + str(index)) from e

        # get values
        try:
            values = self._data[filekey][column].copy()
        except IndexError as e:
            raise self._exception('No values for: ' + str(filekey) + ' column: ' + str(column) + '\n') from e

        return values

    def readFiles(self):
        """
        function to read input files, recognize headings in files
        """
        self._out('Reading files')

        # for all input files
        for filekey in self.file.keys() :
            # open file
            try :
                ifile = open(self._getOption('dir') + '/' + self.file[filekey], 'r')
            except IOError as e :
                raise self._exception('Could not open file: ' + self._getOption('dir') + '/' + self.file[filekey] + '\n') from e

            # create storage
            self._data[filekey] = {}

            # read first line
            line = ifile.readline()

            # get number of columns
            lineData = line.split()
            headings = []

            # test for headings
            idx = 1
            # not sure if there are headings
            if self._getOption('headings') is None:
                try :
                    # headings, go to headings part, dirty
                    if self._getOption('headings') == True:
                        raise ValueError

                    for value in lineData :
                        # try to convert value
                        value = float(value)

                        # create column in storage and assign value
                        self._data[filekey][idx] = []
                        self._data[filekey][idx].append(value)
                        headings.append(idx)
                        idx += 1

                # cannot convert all values
                except ValueError :
                    # print message and store headings
                    self._out('found headings in file: ' + str(filekey))
                    headings = lineData

                    # reset storage
                    self._data[filekey] = {}

                    for heading in headings :
                        self._data[filekey][heading] = []

            for line in ifile :
                if not line.strip():
                    continue

                # split line in data
                lineData = line.split()

                try :
                    for idx in range(0, len(headings)) :
                        # store values
                        self._data[filekey][headings[idx]].append(float(lineData[idx]))
                # conversion error
                except ValueError as e:
                    raise self._exception('Conversion to float of ' + str(lineData[idx]) + ' failed!') from e
                except IndexError as e:
                    raise self._exception('Wrong number of values in one line') from e

            # convert data in numpy vectors
            for key in self._data[filekey].keys() :
                self._data[filekey][key] = numpy.array(self._data[filekey][key])
