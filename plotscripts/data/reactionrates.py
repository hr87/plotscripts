"""
Created on Jun 9, 2013

@author: Hans R Hammer
"""

import numpy

from plotscripts.data.xsdata import XsData


class ReactionRate(XsData):
    """
    executioner for reaction rates extending xsdata for flux map
    data index is the same as xsdata

    :avr type: file type xs | flux
    :var xsfile: cross section file for the flux map
    :var xsMapping: cross section mapping for the flux map

    """

    class File(XsData.File):
        def __init__(self, fileName = ''):
            super().__init__(fileName)
            self.xsFile    = None   # xs for reaction rates for the flux files
            self.xsMapping = None   # mapping for flux files

    def __init__(self):
        super().__init__()

        self.xsfile                   = None      # default xs for reaction rates for the flux files
        self.xsMapping                = []        # default mapping for flux files

        # default file type
        self._addDefault('defaultType', 'flux', 'type of the file flux | xs | pwr | xml', 'private')

        # internal
        self.fluxFileTypes            = {}        # list of all file types containing full xs data
        self.fluxFileTypes['pwr']     = self.readPwrFile
        self.fluxFileTypes['flux']    = self.readFluxFile

        self.fileTypes += list(self.fluxFileTypes.keys())

    def _processClassData(self):
        """
        base method for data processing, called by inputArgs
        reads first all xs files, than all flux maps, maps xs to fluxmaps
        """
        # set up xs
        super()._processClassData()

        # read files
        # for all input files
        for filekey, struct in self.files.items():
            if not struct.type in self.fluxFileTypes:
                continue
            # call stored method
            self.fluxFileTypes[struct.type](filekey)
            # setup all xs and reaction rates, use xs mapping
            self.calcXsData(filekey, struct.xsFile, struct.xsMapping)

    def readFluxFile(self, filekey):
        """
        reads a flux map file
        block group0 group1 ...
        """
        self._out('Reading flux file {0}: {1}'.format(filekey, self.files[filekey].fileName))
        # open file
        try :
            ifile = open(self._getOption('dir') + '/' + self.files[filekey].fileName, 'r')
        except IOError as e:
            raise self._exception('Could not open file: ' + self._getOption('dir') + '/'
                                  + self.files[filekey].fileName + '\n') from e

        # inti storage
        self._data[filekey] = {}

        for line in ifile:
            # check for empty line
            if not line.strip():
                continue

            # split data
            lineData = line.split()

            try:
                blockNr = int(lineData[0])
            except ValueError as e:
                raise self._exception("Could not convert block number") from e

            self._data[filekey][blockNr] = {}
            self._data[filekey][blockNr]['flux'] = []

            # check count
            if len(lineData) != self.numGroups[filekey] + 1:
                raise self._exception('Mismatching number of entries in line')
            # convert line
            for value in lineData[1:]:
                try:
                    self._data[filekey][blockNr]['flux'].append(float(value))
                except ValueError as e:
                    raise self._exception('Error reading value') from e

                    # convert list into numpy array
            self._data[filekey][blockNr]['flux'] = numpy.array(self._data[filekey][blockNr]['flux'])

        ifile.close()

    def readPwrFile(self, filekey):
        """
        reads a power file from rattlesnake
        """
        # number of values in power file to skip
        skippedValuesNum = 6

        self._out('Reading flux file {0}: {1}'.format(filekey, self.files[filekey].fileName))
        # open file
        try :
            ifile = open(self._getOption('dir') + '/' + self.files[filekey].fileName, 'r')
        except IOError as e :
            raise self._exception('Could not open file: ' + self._getOption('dir') + '/'
                                  + self.files[filekey].fileName + '\n') from e

        # inti storage
        self._data[filekey] = {}

        found_block = False

        for line in ifile:
            # check for empty line
            if not line.strip():
                continue

            # skip first first two line
            if 'Block reaction rates' in line:
                found_block = True
                continue
            # found something different
            elif 'reaction rates' in line:
                found_block = False
                continue
            elif 'Blk ID' in line:
                continue

            if found_block:
                # split data
                lineData = line.split()

                try:
                    blockNr = int(lineData[0])
                except ValueError as e:
                    raise self._exception("Could not convert block number") from e

                self._data[filekey][blockNr] = {}
                self._data[filekey][blockNr]['flux'] = []

                # check count
                if len(lineData) != self.numGroups[filekey] + skippedValuesNum:
                    raise self._exception('Mismatching number of entries in line')
                # convert line
                for value in lineData[skippedValuesNum:]:
                    try:
                        self._data[filekey][blockNr]['flux'].append(float(value))
                    except ValueError as e:
                        raise self._exception('Error reading value') from e

                        # convert list into numpy array
                self._data[filekey][blockNr]['flux'] = numpy.array(self._data[filekey][blockNr]['flux'])

        ifile.close()

    def _checkInput(self):
        super()._checkInput()
        # check files
        for filekey, struct in self.files.items():
            # check flux files
            if struct.type in self.fluxFileTypes:
                if not struct.xsFile in self.files:
                    raise self._exception('No xs file for flux/pwr input file {0}'.format(filekey))
                if not self.files[struct.xsFile].type in self.fileTypes:
                    raise self._exception('Xs file must be a xs file for flux file {0}'.format(filekey))

                if not struct.xsMapping.__class__ in [list, numpy.ndarray]:
                    raise self._exception('Xs mapping must be a list for {0}'.format(filekey))
                if struct.xsMapping == []:
                    if self.xsMapping != []:
                        struct.xsMapping = self.xsMapping
                    else:
                        raise self._exception('No xs mapping for {0} and no defaults'.format(filekey))

                #TODO pull xs file group structure
                struct.groupStructure = self.files[struct.xsFile].groupStructure
