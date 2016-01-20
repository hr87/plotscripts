"""
Created on Apr 10, 2013

@author: Hans R Hammer

Executioner for column sorted data
"""

import numpy

from plotscripts.data.basedata import BaseData as _BaseData


class FileData(_BaseData):
    """
    Executioner for column sorted data
    @see BaseValue
    @keyword headings: option Turns on/off headings in input files, default = None, only when first row is not convertable
    """

    class FileIndex(_BaseData.BaseIndex):
        """ Index class for file data

        """
        def __init__(self):
            super().__init__()
            file = None

    @staticmethod
    def index():
        return FileData.FileIndex()

    def __init__(self):
        """
        Constructor
        """
        super().__init__()

        # internal
        self._files = {}  # file names
        self._addDefault('dir', '.', 'folder to look for files', 'private')
        self._addDefault('headings', None, 'Cannot remember', 'private')

    def addFile(self, name, path):
        self._files[name] = path

    def _processClassData(self):
        """
        read and process all the data,
        overwrites base method
        """
        # read input files
        self._readFiles()

    def _getClassData(self, index):
        """ Virtual method to retrieve class data
        :param index: data index
        :return: data as ndarray
        """

        filekey = index.file
        column = index.column

        # get values
        try:
            values = self._data[filekey][column].copy()
        except IndexError as e:
            raise self._exception('No values for: ' + str(filekey) + ' column: ' + str(column) + '\n') from e

        return values

    def _readFiles(self):
        """
        function to read input files, recognize headings in files
        """
        self._out('Reading files')

        # for all input files
        for filekey in self._files.keys():
            # open file
            try:
                ifile = open(self._getOption('dir') + '/' + self._files[filekey], 'r')
            except IOError as e:
                raise self._exception(
                    'Could not open file: ' + self._getOption('dir') + '/' + self._files[filekey] + '\n') from e

            try:
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
                    try:
                        # headings, go to headings part, dirty
                        if self._getOption('headings'):
                            raise ValueError

                        for value in lineData:
                            # try to convert value
                            value = float(value)

                            # create column in storage and assign value
                            self._data[filekey][idx] = []
                            self._data[filekey][idx].append(value)
                            headings.append(idx)
                            idx += 1

                    # cannot convert all values
                    except ValueError:
                        # print message and store headings
                        self._out('found headings in file: ' + str(filekey))
                        headings = lineData

                        # reset storage
                        self._data[filekey] = {}

                        for heading in headings:
                            self._data[filekey][heading] = []

                for line in ifile:
                    if not line.strip():
                        continue

                    # split line in data
                    lineData = line.split()

                    try:
                        for idx, h in enumerate(headings):
                            # store values
                            self._data[filekey][h].append(float(lineData[idx]))
                    # conversion error
                    except ValueError as e:
                        raise self._exception('Conversion to float of ' + str(lineData[idx]) + ' failed!') from e
                    except IndexError as e:
                        raise self._exception('Wrong number of values in one line') from e
            finally:
                ifile.close()

            # convert data in numpy vectors
            for key in self._data[filekey].keys():
                self._data[filekey][key] = numpy.array(self._data[filekey][key])
