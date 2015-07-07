"""
Created on Apr 28, 2013

@author: Hans R Hammer

Defines an exception class
"""

class PlotscriptException(Exception):
    """
     Exception class for plot exceptions, normally created by function exception of BaseObject
     :var module: name of calling module
     :var function: name of calling function
     :var msg: message text
     """
    module = None
    function = None
    msg = None

    def __init__(self, module, function, msg):
        """ Constructor
        :param module: Calling module name
        :param function: Calling function name
        :param msg: message text
        """
        self.module = module
        self.function = function
        self.msg = msg

    def __str__(self, *args, **kwargs):
        tmpStr = 'Exception in Module: {0}\n'.format(self.module)
        tmpStr += 'Function {0}; {1}'.format(self.function, self.msg)

        if self.__cause__:
            tmpStr += '\n{0}'.format(self.__cause__)

        return tmpStr