"""
Created on Apr 24, 2013

@author: Hans R Hammer
"""

def axisDiv(axRange, axMag):
    """ Calculate a divisor for an axis

    :param axRange: range of an axis
    :param axMag: the magnitude of an axis
    :return: axis divisor
    """
    if axRange <= axMag * 2 :
        return 4
    elif axRange <= axMag * 5 :
        return 2
    else :
        return 1
