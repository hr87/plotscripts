"""
Created on May 12, 2013

@author: Hans R Hammer

Provides a geometry for basic x-y read from a file
"""

import numpy
from plotscripts.geometry.basegeometry import BaseGeometry

class BaseXYGeometry(BaseGeometry):
    """
    Creates a base geometry for for xy points read from a file
    @var fileName: file name of file with points
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.fileName = ''

        self.xyPoints = None    # numpy array for points

    def readPoints(self, filename):

        # open file to read
        try:
            pointFile = open(filename, 'r')
        except IOError as e:
            raise self.exception('Could no open point file {0}'.format(filename)) from e

        # tmp list for read data
        points = []
        try:
            for line in pointFile:
                # check for empty line
                if not line.strip():
                    continue
                # split line
                lineData = line.split()
                # convert and append
                points.append([float(lineData[0]), float(lineData[1])])

            pointFile.close()

        # catch reading and converting errors
        except IOError as e:
            raise self.exception('Error reading file {0}'.format(filename)) from e
        except TypeError as e:
            raise self.exception('Error converting points to float') from e
        # convert tmp list into numpy array
        self.xyPoints = numpy.array(points)

