"""
Created on Apr 16, 2013

@author: Hans R Hammer
"""

import numpy
from plotscripts.data.basedata import BaseData
from plotscripts.base.basecontainer import BaseContainer
numpy.set_printoptions(threshold=numpy.nan)

class XsData(BaseData):
    """ executioner for cross section data and reaction rates
    data index: file [, material [, groups]]
    material select with list or None for all
    groups select with list or None for all or -1 for sum

   :var groupStrucur: list with energy boundaries, one more than count of groups
    "var volumes: List of volumes for normalization of the flux for an input, default is None
    """

    class File(BaseContainer):
        def __init__(self, fileName = ''):
            super().__init__()
            self.fileName           = fileName           # file name
            self.groupStructure     = []                 # energy group structure, provide for each single input or as list for all
            self.volumes            = None               # volumes for normalization
            self.type               = ''                 # type of file

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.files              = {}                 # file names
        self.groupStructure     = []                 # energy group structure, provide for each single input or as list for all
        self.xLabel             = 'Energy [MeV]'
        self.volumes            = {}                 # volumes for normalization
        self.type = {}                               # type of file

        self._defaults['dir']          = '.'          # folder to look for files
        self._defaults['xScale']       = 'log'        # default scale for line plots
        self._defaults['cutoff']       = 1e-10        # smallest value
        self._defaults['flux_norm']    = 'sum'        # method to normalize flux 'sum' | 'avg' | 'max'
        self._defaults['defaultType']  = 'xs'          # type of the file xs | xml
        self.columns   = ['flux', 'total', 'diffusion', 'nufission', 'fission',
                          'absorption', 'chi', 'kappa', 'scattering', 'capture',
                          'removal', 'fission_rate', 'nufission_rate', 'total_rate',
                          'capture_rate', 'absorption_rate', 'removal_rate', 'k_inf',
                          'mfactor', 'flux_norm', 'power']    # columns for statistics, can be overwritten for each statistic

        # internal
        self.numGroups            = {}          # number of groups
        self.xsFileTypes          = {}          # available file types with reading function
        self.xsFileTypes['xs']    = self.readXsFile
        self.xsFileTypes['xml']   = self.readXmlFile

        self.fileTypes = list(self.xsFileTypes.keys())

    def _processClassData(self):
        """
        base method for data processing, called by inputArgs
        read xs files
        """
        # create dict
        self.xSteps = {}

        # prepare groups and x values
        for key, struct in self.files.items():
            # number of groups
            #TODO number of groups for each file
            self.numGroups[key] = struct.groupStructure.size - 1

            # log mean values
            self.xSteps[key] = numpy.power(10 * numpy.ones(self.numGroups[key]), (numpy.log10(struct.groupStructure[:-1]) + numpy.log10(struct.groupStructure[1:])) / 2)

        # read files
        # for all input files
        for filekey, struct in self.files.items():
            if not struct.type in self.xsFileTypes:
                continue
            # call stored method
            self.xsFileTypes[struct.type](filekey)
            # calculate remaining xs data and reaction rates
            self.calcXsData(filekey)

        # link x values for statistics, first entry at the moment
        for statistic in self._statistics:
            self.xSteps[statistic] = self.xSteps[self._statistics[statistic].input[0][0]]

    def getClassData(self, index):
        """
        base interface method for plotter to get data, returns the corresponding data for file index, column index
        methods available are: value, diff, rel
        index:
        @param index: list with index of data
        @return: numpy array with data
        """
        if len(index) == 2:
            filekey     = index[0]
            materials   = None
            groups      = None
            column      = index[1]
        elif len(index) == 3:
            filekey     = index[0]
            materials   = index[1]
            groups      = None
            column      = index[2]
        elif len(index) == 4:
            filekey     = index[0]
            materials   = index[1]
            groups      = index[2]
            column      = index[3]
        else:
            raise self._exception('Wrong index: ' + str(index))

        if not filekey in self.files:
            raise self._exception('Could not find file {0}'.format(filekey))

        # initlize value lists
        values = []

        # get the all operator
        if materials is None:
            materials = sorted(self._data[filekey].keys())
        elif materials.__class__ != list:
            materials = [materials]
        if groups is None:
            groups = list(range(self.numGroups[filekey]))
        elif groups.__class__ != list:
            groups = [groups]

        # get all materials
        for material in materials:
            # get values
            try:
                if column == 'k_inf':
                    y = numpy.array([self._data[filekey][material][column][0]] * len(groups)).squeeze()
                elif column == 'mfactor':
                    # get nufisison and absorption reaction rates
                    nufis = self.getClassData([filekey, material, groups, 'nufission_rate'])
                    absR = self.getClassData([filekey, material, groups, 'absorption_rate'])

                    y = nufis / absR
                elif groups == [-1]:
                    y = numpy.nansum(self._data[filekey][material][column])
                else:
                    y = numpy.zeros((len(groups)))

                    # pick or condense groups
                    for idxGroup, group in enumerate(groups):
                        # condense
                        if group.__class__ == list:
                            y[idxGroup] = 0
                            for g in group:
                                y[idxGroup] += self._data[filekey][material][column][g]
                        else:
                            y[idxGroup] = self._data[filekey][material][column].copy()[group]
            except (IndexError, KeyError) as e:
                raise self._exception('No values for index ({0}, {1}, {2}, {3})'.format(filekey, material, groups, column)) from e

            values.append(y)

        if len(values) > 1:
            values = numpy.array(values)
        else:
            values = values[0]

        return values

    def getXValues(self, index, column):
        """
        get standard x values
        @return: numpy array with x values
        """
        # check for statistics
        try:
            return self.xSteps[index[0]].copy()
        except KeyError as e:
            raise self._exception('No x values for {0}'.format(index[0])) from e

    def readXsFile(self, filekey):
        """
        function to read input xs files and store data
        reads also xs files with scattering > P0, ignores higher order
        """

        self._out('Reading xs file {0}: {1}'.format(filekey, self.files[filekey].fileName))
        # open file
        try:
            ifile = open(self._getOption('dir') + '/' + self.files[filekey].fileName, 'r')
        except IOError as e:
            raise self._exception('Could not open file: ' + self._getOption('dir') + '/' + self.files[filekey].fileName + '\n') from e

        # create storage
        self._data[filekey] = {}

        # material index
        matNr = 0
        group = None

        # read all lines
        for line in ifile:

            # search for the beginning of material
            if 'MATERIAL' in line:
                # increase material number
                matNr += 1
                # create new material
                self._data[filekey][matNr] = {}
                self._data[filekey][matNr]['flux'] = numpy.zeros(self.numGroups[filekey])
                self._data[filekey][matNr]['total'] = numpy.zeros(self.numGroups[filekey])
                self._data[filekey][matNr]['diffusion'] = numpy.zeros(self.numGroups[filekey])
                self._data[filekey][matNr]['nufission'] = numpy.zeros(self.numGroups[filekey])
                self._data[filekey][matNr]['fission'] = numpy.zeros(self.numGroups[filekey])
                self._data[filekey][matNr]['chi'] = numpy.zeros(self.numGroups[filekey])
                self._data[filekey][matNr]['absorption'] = numpy.zeros(self.numGroups[filekey])
                self._data[filekey][matNr]['kappa'] = numpy.zeros(self.numGroups[filekey])
                # read one material
                for matLine in ifile:

                    # test for empty line
                    if not matLine.strip():
                        continue

                    # test for end of xs block
                    if 'Scattering Profile' in matLine:
                        break

                    # read cross sections
                    # split line in data
                    lineData = matLine.split()

                    try:
                        # current group
                        group = int(lineData[0]) - 1
                        # and the good stuff
                        self._data[filekey][matNr]['flux'][group]        = float(lineData[1])
                        self._data[filekey][matNr]['total'][group]       = float(lineData[2])
                        self._data[filekey][matNr]['diffusion'][group]   = float(lineData[3])
                        self._data[filekey][matNr]['nufission'][group]   = float(lineData[4])
                        self._data[filekey][matNr]['fission'][group]     = float(lineData[5])
                        self._data[filekey][matNr]['chi'][group]         = float(lineData[6])
                        self._data[filekey][matNr]['absorption'][group]  = float(lineData[7])
                        self._data[filekey][matNr]['kappa'][group]       = float(lineData[8])

                    except ValueError as e:
                        raise self._exception('Conversion to float of ' + str(matLine) + ' failed!') from e
                    except IndexError as e:
                        raise self._exception('Wrong number of values! File {0}; material {1}; group {2}'.format(filekey, matNr, group)) from e

                if (group + 1) != self.numGroups[filekey]:
                    raise self._exception('Wrong number of groups: file {0}; material {1}, groups {2}'.format(filekey, matNr, group + 1))

                # read scattering profile
                profile = []
                group = 0
                p1Scattering = False

                for matLine in ifile:
                    # test for empty line
                    if not matLine.strip():
                        continue

                    # split line
                    lineData = matLine.split()

                    # test for higher order scattering
                    p1Scattering = len(lineData) >= 4

                    try:
                        # get the first 2 entries
                        profile.append((int(lineData[0]) - 1, int(lineData[1])))

                    except ValueError as e:
                        raise self._exception('Conversion to int of ' + str(matLine) + ' failed!') from e
                    except IndexError as e:
                        raise self._exception('Missing values in profile for group ' + str(group) + ' and Material ' + str(matNr)) from e

                    # increase counter
                    group += 1

                    # test for end of profile block
                    if not group < self.numGroups[filekey]:
                        break

                group = 0
                matLine = None
                # create scattering matrix
                self._data[filekey][matNr]['ScatMatrix'] = numpy.zeros((self.numGroups[filekey], self.numGroups[filekey]))

                # read scattering matrix
                for matLine in ifile:
                    # test for end of P0 scattering
                    if group == self.numGroups[filekey]:
                        break

                        # test for empty scattering lines
                    if profile[group][0] >= self.numGroups[filekey]:
                        group += 1

                    # test for end of P0 scattering
                    if group == self.numGroups[filekey]:
                        break

                        # test for empty line
                    if not matLine.strip():
                        continue

                    # test for end of xs block
                    if '/MATERIAL' in matLine:
                        if group != self.numGroups[filekey]:
                            raise self._exception('Wrong number of groups in scattering for ' + str(filekey) + ' and Material ' + str(matNr))
                        break

                    # split
                    lineData = matLine.split()

                    try:
                        # read and assing using profile
                        self._data[filekey][matNr]['ScatMatrix'][group, profile[group][0]:profile[group][1]] = [float(i) for i in lineData]
                    except ValueError as e:
                        raise self._exception('Conversion to float of ' + str(matLine) + ' failed!') from e
                    except IndexError as e:
                        raise self._exception('Missing values in scattering matrix for group ' + str(group) + ' and Material ' + str(matNr)) from e

                    group += 1

                    # test for end of P0 scattering
                    if group == self.numGroups[filekey] and p1Scattering:
                        break

                        # search material end
                if '/MATERIAL' not in matLine:
                    for matLine in ifile:
                        if '/MATERIAL' in matLine:
                            break

    def readXmlFile(self, filekey):
        """
        function to read input xs files and store data
        reads also xs files with scattering > P0, ignores higher order
        """
        import defusedxml.pulldom as xmlParser
        import xml.sax
        import xml.dom.pulldom as pulldom

        mapping = {
            'volume': 'Volume',
            'total': 'TotalXS',
            'flux': 'Flux',
            'diffusion': 'DiffusionCoefficient',
            'absorption': 'AbsorptionXS',
            'fission': 'FissionXS',
            'nufission': 'NuFissionXS',
            'kappa': 'KappaXS',
            'chi': 'ChiXS',
            'profile': 'Profile',
            'scatMatrix': 'ScatteringXS',
        }

        fissileList = ['total', 'diffusion', 'absorption', 'fission', 'nufission', 'chi', 'flux']
        nonFissileList = ['total', 'diffusion', 'absorption', 'flux']
        naList = ['kappa']

        self._out('Reading xs file {0}: {1}'.format(filekey, self.files[filekey].fileName))
        # open file
        try:
            xmlFile = open(self._getOption('dir') + '/' + self.files[filekey].fileName, 'r')
        except IOError as e:
            raise self._exception('Could not open file: ' + self._getOption('dir') + '/' + self.files[filekey].fileNames + '\n') from e

        # create storage
        self._data[filekey] = {}

        try:
            # parse file with pulldom
            try:
                document = xmlParser.parse(xmlFile)
            except xml.sax.SAXException as e:
                raise self._exception('Error while parsing xml file {0}'.format(self.files[filekey].fileName)) from e

            # iterate over all event in document, looking for header
            for event, node in document:
                if event == pulldom.START_ELEMENT and node.tagName == 'Macros':
                    try:
                        numGroups = int(node.getAttribute('NG'))
                    except ValueError as e:
                        raise self._exception('Could not convert groups into integer') from e
                    if self.numGroups[filekey] != numGroups:
                        raise self._exception('Number of groups not matching in file: {0} and {1}'.format(self.numGroups[filekey], numGroups))

                # found header element
                if event == pulldom.START_ELEMENT and node.tagName == 'material':
                    # read the full node
                    document.expandNode(node)

                    # get material and fissile
                    try:
                        matNr = int(node.getAttribute('ID'))
                    except ValueError as e:
                        raise self._exception('Could not convert material Id')
                    fissile = node.getAttribute('fissile').lower() == 'true'

                    # create new material entry
                    self._data[filekey][matNr] = {}

                    # read xs
                    if fissile:
                        xsList = fissileList
                    else:
                        xsList = nonFissileList

                    for xsType in xsList:
                        # create xs storage
                        self._data[filekey][matNr][xsType] = []
                        # get node
                        xsNode = self.getNode(node, mapping[xsType])
                        # get node data
                        nodeData = self.getNodeText(xsNode).split()

                        if not len(nodeData) == self.numGroups[filekey]:
                            raise self._exception('Number of groups not matching for {0} in material {1}'.format(mapping[xsType], matNr))

                        for value in nodeData:
                            try:
                                self._data[filekey][matNr][xsType].append(float(value))
                            except ValueError as e:
                                raise self._exception('Could not convert value in for {0} in material {1}'.format(mapping[xsType], matNr)) from e

                        # convert to numpy
                        self._data[filekey][matNr][xsType] = numpy.array(self._data[filekey][matNr][xsType])

                    # populate remaining arrays
                    if not fissile:
                        for xsType in fissileList:
                            if not xsType in nonFissileList:
                                self._data[filekey][matNr][xsType] = numpy.zeros((self.numGroups[filekey]))

                    for xsType in naList:
                        self._data[filekey][matNr][xsType] = numpy.zeros((self.numGroups[filekey]))

                    # read scattering profile
                    xsNode = self.getNode(node, mapping['profile'])
                    nodeData = self.getNodeText(xsNode).split()

                    if len(nodeData) == 0 or len(nodeData) % self.numGroups[filekey] != 0:
                        raise self._exception('Scattering profile messed up for material {0}'.format(matNr))

                    profile = numpy.zeros((self.numGroups[filekey], 2), numpy.int8)
                    for idx in range(self.numGroups[filekey]):
                        try:
                            profile[idx, 0] = int(nodeData[2*idx]) - 1
                            profile[idx, 1] = int(nodeData[2*idx+1])
                        except ValueError as e:
                            raise self._exception('Could not convert value into integer for the scattering profile for material {0}'.format(matNr)) from e

                    # create scattering matrix
                    self._data[filekey][matNr]['ScatMatrix'] = numpy.zeros((self.numGroups[filekey], self.numGroups[filekey]))

                    xsNode = self.getNode(node, mapping['scatMatrix'])
                    nodeData = self.getNodeText(xsNode).split()

                    idx = 0
                    for group in range(self.numGroups[filekey]):
                        # test for empty scattering lines
                        if profile[group, 0] >= self.numGroups[filekey]:
                            continue
                        # number of scattering values for group
                        num = profile[group, 1] - profile[group, 0]

                        try:
                            # read and assign using profile
                            self._data[filekey][matNr]['ScatMatrix'][group, profile[group, 0]:profile[group, 1]] = [float(nodeData[i]) for i in range(idx, idx + num)]
                        except ValueError as e:
                            raise self._exception('Could not convert value into float for the scattering matrix for material {0}'.format(matNr)) from e
                        except IndexError as e:
                            raise self._exception('Missing values in scattering matrix for group {0} and material {1}'.format(group, matNr)) from e

                        # increase position
                        idx += num

        finally:
            xmlFile.close()

    def calcXsData(self, filekey, baseXsKey = None, xsMapping = None):
        """
        function to calculate missing xs
        """
        self._debug('calcData for {0}'.format(filekey))

        flux = numpy.zeros((len(self._data[filekey]), self.numGroups[filekey]))
        materials = sorted(self._data[filekey].keys())

        for idxMat, material in enumerate(materials):
            # get all fluxes
            flux[idxMat,:] = self._data[filekey][material]['flux']

        # normalize flux, can be set by option
        if self._getOption('flux_norm') == 'avg':
            try:
                flux /= numpy.average(flux, 0, self.volumes[filekey]).mean()
            except ValueError as e:
                raise self._exception('Averaging failed, number values: {0}, number weights {1}'.format(flux.shape, self.volumes[filekey].shape)) from e
        elif self._getOption('flux_norm') == 'sum':
            flux /= flux.sum()
        elif self._getOption('flux_norm') == 'max':
            flux /= numpy.nanmax(flux)
        else:
            raise self._exception('Unknown normalization for flux')

        # write fluxes back
        for idxMat, material in enumerate(materials):
            self._data[filekey][material]['flux'][:] = flux[idxMat,:]

        # calculate missing cross sections and reaction rates
        for idxMaterial, material in enumerate(materials):
            # prepare volume for reaction rates
            if self.files[filekey].volumes is None:
                volume = 1
            else:
                volume = self.files[filekey].volumes[idxMaterial]

            # get flux
            flux = self._data[filekey][material]['flux']
            # get base material
            if baseXsKey is None:
                baseMaterial = self._data[filekey][material]

                # set cutoffs
                baseMaterial['flux'][numpy.abs(baseMaterial['flux']) < self._getOption('cutoff')] = float('NaN')
                baseMaterial['total'][numpy.abs(baseMaterial['total']) < self._getOption('cutoff')] = float('NaN')
                baseMaterial['diffusion'][numpy.abs(baseMaterial['diffusion']) < self._getOption('cutoff')] = float('NaN')
                baseMaterial['nufission'][numpy.abs(baseMaterial['nufission']) < self._getOption('cutoff')] = float('NaN')
                baseMaterial['fission'][numpy.abs(baseMaterial['fission']) < self._getOption('cutoff')] = float('NaN')
                baseMaterial['absorption'][numpy.abs(baseMaterial['absorption']) < self._getOption('cutoff')] = float('NaN')

            else:
                if xsMapping is None:
                    baseMaterial = self._data[baseXsKey][idxMaterial + 1]
                else:
                    baseMaterial = self._data[baseXsKey][xsMapping[idxMaterial]]
                # copy cross sections
                #TODO copy, ref possible?
                self._data[filekey][material]['total'] = baseMaterial['total'].copy()
                self._data[filekey][material]['diffusion'] = baseMaterial['diffusion'].copy()
                self._data[filekey][material]['nufission'] = baseMaterial['nufission'].copy()
                self._data[filekey][material]['fission'] = baseMaterial['fission'].copy()
                self._data[filekey][material]['chi'] = baseMaterial['chi'].copy()
                self._data[filekey][material]['absorption'] = baseMaterial['absorption'].copy()
                self._data[filekey][material]['kappa'] = baseMaterial['kappa'].copy()

            # calc remaining xs
            self._data[filekey][material]['scattering'] = baseMaterial['ScatMatrix'].sum(0)
            self._data[filekey][material]['capture'] = baseMaterial['absorption'] - baseMaterial['fission']
            self._data[filekey][material]['removal'] = baseMaterial['total'] - baseMaterial['ScatMatrix'].diagonal()

            # calc reaction rates
            self._data[filekey][material]['fission_rate'] = baseMaterial['fission'] * flux * volume
            self._data[filekey][material]['nufission_rate'] = baseMaterial['nufission'] * flux * volume
            self._data[filekey][material]['total_rate'] = baseMaterial['total'] * flux * volume
            self._data[filekey][material]['capture_rate'] = baseMaterial['capture'] * flux * volume
            self._data[filekey][material]['absorption_rate'] = baseMaterial['absorption'] * flux * volume
            self._data[filekey][material]['removal_rate'] = baseMaterial['removal'] * flux * volume
            # power
            self._data[filekey][material]['power'] = baseMaterial['kappa'] * self._data[filekey][material]['fission_rate']
            # k_inf
            self._data[filekey][material]['k_inf'] = (self._data[filekey][material]['nufission_rate'].sum() / self._data[filekey][material]['absorption_rate'].sum()).repeat(self.numGroups[filekey])

            # calculate spectrum
            groupStructure = self.files[filekey].groupStructure
            self._data[filekey][material]['flux_norm'] = 1.0 / flux.sum() * (flux / (numpy.log10(groupStructure[:-1]) - numpy.log10(groupStructure[1:])))

    def _checkInput(self):
        """
        check the input and convert if necessary
        """
        super()._checkInput()

        if not self.groupStructure.__class__ == list:
            raise self._exception('Wrong format for group structure')

        # convert volumes
        for key, struct in self.files.items():
            if struct.fileName == '':
                raise self._exception('No file name given for {0}'.format(key))
            if struct.fileName.__class__ != str:
                raise self._exception('File name must be a string for {0}'.format(key))
            if not struct.groupStructure.__class__ in [list, numpy.ndarray]:
                raise self._exception('Group structure must be a list for {0}'.format(key))
            if struct.groupStructure == []:
                if self.groupStructure != []:
                    struct.groupStructure = self.groupStructure
                else:
                    raise self._exception('No group structure for {0} and no defaults'.format(key))

            struct.groupStructure = numpy.array(struct.groupStructure)

            if struct.volumes is not None and struct.volumes.__class__ != list:
                raise self._exception('Wrong type for volumes in {0}'.format(key))
            if struct.volumes.__class__ == list:
                struct.volumes = numpy.array(struct.volumes)
            if struct.type.__class__ != str:
                raise self._exception('Wrong type for file type in {0}'.format(key))
            if struct.type == '':
                struct.type = self._getOption('defaultType')
            # TODO check type
            if not struct.type in self.fileTypes:
                raise self._exception('Unknown file type {0} for {1}'.format(struct.type, key))

    def getYLabel(self, column, method = 'value'):
        """
        get y label for data
        @return: label as string
        """

        if method == 'value':
            if column == 'flux':
                return 'Flux [1/cm^2]'
            elif column == "flux_norm":
                return 'Neutron flux / Lethargy (normalized)'
            elif column == "total":
                return 'Sigma t'
                # label = '\Sigma _{tot}';
            elif column == "diffusion":
                return 'Diffusion coefficient D'
            elif column == "nufission":
                return 'nu Sigma f'
                # label = '\nu\Sigma_f';
            elif column == "fission":
                return 'Sigma f'
                # label = '\Sigma _f';
            elif column == "chi":
                return 'Chi'
            elif column == "absorption":
                return 'Sigma a'
                # label = '\Sigma _a';
            elif column == "kappa":
                return 'kappa'
                # label = '\kappa';
            elif column == 'scat':
                return 'Sigma S'
                # label = '\Sigma _S';
            elif column == 'fission_rate':
                return 'fission rate'
            elif column == 'nufission_rate':
                return 'nu * fission rate'
            elif column == 'capture_rate':
                return 'capture rate'
            elif column == 'absorption_rate':
                return 'absorption rate'
            elif column == 'removal_rate':
                return 'removal rate'
            else:
                return str(column)
        elif method == 'diff':
            if column == 'flux':
                return 'Delta Flux [1/cm^2]'
            elif column == "flux_norm":
                return 'Delta Neutron flux / Lethargy (normalized)'
            elif column == "total":
                return 'Delta Sigma t'
                # label = '\Sigma _{tot}';
            elif column == "diffusion":
                return 'Delta Diffusion coefficient D'
            elif column == "nufission":
                return 'Delta nu Sigma f'
                # label = '\nu\Sigma_f';
            elif column == "fission":
                return 'Delta Sigma f'
                # label = '\Sigma _f';
            elif column == "chi":
                return 'Delta Chi'
            elif column == "absorption":
                return 'Delta Sigma a'
                # label = '\Sigma _a';
            elif column == "kappa":
                return 'Delta kappa'
                # label = '\kappa';
            elif column == "scat":
                return 'Delta Sigma S'
                # label = '\Sigma _S'
            elif column == 'fission_rate':
                return 'Delta fission rate'
            elif column == 'nufission_rate':
                return 'Delta nu * fission rate'
            elif column == 'capture_rate':
                return 'Delta capture rate'
            elif column == 'absorption_rate':
                return 'Delta absorption rate'
            elif column == 'removal_rate':
                return 'Delta removal rate'
            else:
                return str(column)
        elif method == 'rel':
            return 'Deviation in %'

    def getNode(self, node, tag):
        # read phase and exercise
        tmpList = node.getElementsByTagName(tag)
        # check for double nodes
        if len(tmpList) > 1:
            raise self._exception('Duplicate entry for {0} found'.format(tag))
        # check for empty list
        elif len(tmpList) < 1:
            raise self._exception('{0} tag not found in node {1}'.format(tag, node))

        # get node
        return tmpList[0]

    def getNodeText(self, node):
        try:
            tmp = [tmp.nodeValue for tmp in node.childNodes]
            tmpStr = ''.join(tmp).strip()
        except TypeError as e:
            raise self._exception('Reading text from node {0} failed'.format(node)) from e
        return tmpStr
