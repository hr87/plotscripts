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

        self.defaults['offsetX']         = 0            # move geometry in x direction
        self.defaults['offsetY']         = 0            # move geometry in y direction
        self.defaults['rotation']        = 0            # rotation around z axis
        self.defaults['offsetXRot']      = 0            # translate x before rotate
        self.defaults['offsetYRot']      = 0            # translate y before rotate
        self.defaults['flipX']           = False        # flip horizontally
        self.defaults['flipY']           = False        # flip vertically

        self.dimensions     = 'mm'      # dimensions

    def setupGeometry(self):
        self.out('Setting up geometry')
        self.activateDefaults()

        self.setupClassGeometry()

    def transform(self, points):
        self.debug('Transform with (x,y,alpha) = ({0},{1},{2})'.format(self.options['offsetX'], self.options['offsetY'], self.options['rotation']))
        # first create copy
        points = points.copy()

        # flip
        if self.options['flipX']:
            points[:, 0] *= -1
        if self.options['flipY']:
            points[:, 1] *= -1

        # translate
        points[:, 0] += self.options['offsetXRot']
        points[:, 1] += self.options['offsetYRot']

        # rotate
        angle = self.options['rotation']
        # create an empty array
        tmpPoints = numpy.zeros(points.shape)
        # calculate rotation
        tmpPoints[:, 0] = points[:, 0] * numpy.cos(angle) - points[:, 1] * numpy.sin(angle)
        tmpPoints[:, 1] = points[:, 0] * numpy.sin(angle) + points[:, 1] * numpy.cos(angle)
        # assign new values to points
        points = tmpPoints

        # translate
        points[:, 0] += self.options['offsetX']
        points[:, 1] += self.options['offsetY']

        return points

    def getValuePaths(self):
        self.debug('getValuePaths')
        return self.transform(self.getClassValuePaths())

    def getOverlayPaths(self):
        self.debug('getOverlayPaths')
        return self.transform(self.getClassOverlayPaths())

    def getTextPoints(self):
        self.debug('getTextPoints')
        return self.transform(self.getClassTextPoints())

    def getValuePoints(self):
        self.debug('getValuePoints')
        return self.transform(self.getClassValuePoints())

    def getExtrema(self, valuePaths, data):
        # init array
        extrema = [0, 0, 0 ,0]

        if data == None or numpy.all(numpy.isnan(data)):
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
        self.debug('getPathTypes')
        return self.getClassPathTypes()

    def getOverlayTypes(self):
        self.debug('getPathTypes')
        return self.getClassOverlayTypes()

    def checkInput(self):
        pass

    def getXLabel(self):
        return 'x [{0}]'.format(self.dimensions)

    def getYLabel(self):
        return 'y [{0}]'.format(self.dimensions)

    # prototypes for class methods
    def setupClassGeometry(self):
        raise self.exception('Not implemented yet')

    def getClassValuePaths(self):
        raise self.exception('Not implemented yet')

    def getClassOverlayPaths(self):
        raise self.exception('Not implemented yet')

    def getClassTextPoints(self):
        raise self.exception('Not implemented yet')

    def getClassValuePoints(self):
        raise self.exception('Not implemented yet')

    def getClassPathTypes(self):
        raise self.exception('Not implemented yet')

    def getClassOverlayTypes(self):
        raise self.exception('Not implemented yet')
 
