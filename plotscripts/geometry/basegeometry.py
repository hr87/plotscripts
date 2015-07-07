"""
Created on Apr 22, 2013

@author: Hans R Hammer
"""

import numpy

from plotscripts.base.baseobject import BaseObject


class BaseGeometry(BaseObject):
    """
    classdocs
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()

        self._addDefault('offsetX', 0, 'move geometry in x direction', 'private')
        self._addDefault('offsetY', 0, 'move geometry in y direction', 'private')
        self._addDefault('rotation', 0, 'rotation around z axis', 'private')
        self._addDefault('offsetXRot', 0, 'translate x before rotate', 'private')
        self._addDefault('offsetYRot', 0, 'translate y before rotate', 'private')
        self._addDefault('flipX', False, 'flip horizontally', 'private')
        self._addDefault('flipY', False, 'flip vertically', 'private')
        self._addDefault('dimensions', 'mm', 'dimensions', 'private')

    def setupGeometry(self):
        self._out('Setting up geometry')
        self._activateDefaults()
        self.setupClassGeometry()

    def transform(self, points):
        self._debug('Transform with (x,y,alpha) = ({0},{1},{2})'.format(self._getOption('offsetX'),
                                                                        self._getOption('offsetY'),
                                                                        self._getOption('rotation')))
        # first create copy
        points = points.copy()

        # flip
        if self._getOption('flipX'):
            points[:, 0] *= -1
        if self._getOption('flipY'):
            points[:, 1] *= -1

        # translate
        points[:, 0] += self._getOption('offsetXRot')
        points[:, 1] += self._getOption('offsetYRot')

        # rotate
        angle = self._getOption('rotation')
        # create an empty array
        tmpPoints = numpy.zeros(points.shape)
        # calculate rotation
        tmpPoints[:, 0] = points[:, 0] * numpy.cos(angle) - points[:, 1] * numpy.sin(angle)
        tmpPoints[:, 1] = points[:, 0] * numpy.sin(angle) + points[:, 1] * numpy.cos(angle)
        # assign new values to points
        points = tmpPoints

        # translate
        points[:, 0] += self._getOption('offsetX')
        points[:, 1] += self._getOption('offsetY')

        return points

    def getValuePaths(self):
        self._debug('getValuePaths')
        return self.transform(self.getClassValuePaths())

    def getOverlayPaths(self):
        self._debug('getOverlayPaths')
        return self.transform(self.getClassOverlayPaths())

    def getTextPoints(self):
        self._debug('getTextPoints')
        return self.transform(self.getClassTextPoints())

    def getValuePoints(self):
        self._debug('getValuePoints')
        return self.transform(self.getClassValuePoints())

    def getExtrema(self, valuePaths, data):
        # init array
        extrema = [0, 0, 0 ,0]

        if data is None or numpy.all(numpy.isnan(data)):
            # get values
            extrema[0] = numpy.nanmin(valuePaths[:, 0, :])
            extrema[1] = numpy.nanmax(valuePaths[:, 0, :])
            extrema[2] = numpy.nanmin(valuePaths[:, 1, :])
            extrema[3] = numpy.nanmax(valuePaths[:, 1, :])
        else :
            # get values
            extrema[0] = numpy.nanmin(valuePaths[~numpy.isnan(data), 0, :])
            extrema[1] = numpy.nanmax(valuePaths[~numpy.isnan(data), 0, :])
            extrema[2] = numpy.nanmin(valuePaths[~numpy.isnan(data), 1, :])
            extrema[3] = numpy.nanmax(valuePaths[~numpy.isnan(data), 1, :])

        return extrema

    def getPathTypes(self):
        self._debug('getPathTypes')
        return self.getClassPathTypes()

    def getOverlayTypes(self):
        self._debug('getPathTypes')
        return self.getClassOverlayTypes()

    def _checkInput(self):
        pass

    def getXLabel(self):
        return 'x [{0}]'.format(self.dimensions)

    def getYLabel(self):
        return 'y [{0}]'.format(self.dimensions)

    # prototypes for class methods
    def setupClassGeometry(self):
        raise self._exception('Not implemented in base class')

    def getClassValuePaths(self):
        raise self._exception('Not implemented in base class')

    def getClassOverlayPaths(self):
        raise self._exception('Not implemented in base class')

    def getClassTextPoints(self):
        raise self._exception('Not implemented in base class')

    def getClassValuePoints(self):
        raise self._exception('Not implemented in base class')

    def getClassPathTypes(self):
        raise self._exception('Not implemented in base class')

    def getClassOverlayTypes(self):
        raise self._exception('Not implemented in base class')
