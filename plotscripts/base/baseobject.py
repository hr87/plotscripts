"""
Created on Apr 26, 2013

@author: Hans R Hammer

Provides a base object for all modules.
All used modules must inherit from this class
"""

from plotscripts.base.exception import PlotscriptException

import inspect

class BaseObject(object):
    """
    Base object class for all used objects
    providing basic functions for option managment, exception creating
    and output
    :var options: dict with options, set by user or using defaults
    :var defaults: dict with default values for options
    :var debugging: option, turns on debbuging for all objects
    """

    debugging = False
    Exception = PlotscriptException

    def __init__(self):
        """
        Constructor
        """
        self.options     = {}       # dict for user set options
        self.defaults    = {}       # dict for default options

        self.defaults['debug'] = False
        self.defaults['pathrepl']    = {'.':'', ' ':'_', '//':'/', '-':'_'}

    def setOptions(self, options):
        """
        Setting options in object without overwriting existing ones
        :param options: options to set in this object
        """
        for option in options :
            if not option in self.options :
                self.options[option] = options[option]

    #TODO have to think about that
    def getOptions(self, pObject):
        """
        getting options from an object without overwriting
        @param get options from an object, must be a subclass of BaseObject
        """
        if not issubclass(pObject.__class__, BaseObject):
            raise self.exception('{0} is not a valid module'.format(pObject.__class__.__name__))

        for option in pObject.options :
            if not option in self.options :
                self.options[option] = pObject.options[option]

    def activateDefaults(self):
        """
        set missing options to defaults
        """
        # setting remaining defaults
        for option in self.defaults:
            if not option in self.options:
                self.options[option] = self.defaults[option]


    def exception(self, msg):
        """
        Creates and return an exception
        @param msg: message text for exception
        @return: exception
        """
        # get class name
        module      = self.__class__.__name__
        # get function name
        function    = inspect.stack()[1][3]
        # create exception
        return PlotscriptException(module, function, msg)

    def out(self, msg):
        """
        Prints a message
        :param msg: message text
        """
        # get class name
        module  = self.__class__.__name__
        tmpStr  = '{0}: {1}'.format(module, msg)
        print(tmpStr)

    def debug(self, msg):
        """
        Prints a debbuging message, only if option debug is set
        :param msg: message text
        """
        if self.debugging or self.options['debug']:
            # get class name
            module  = self.__class__.__name__
            tmpStr  = '{0}: {1}'.format(module, msg)
            print(tmpStr)

    def error(self, msg):
        """
        prints an error msg
        :param msg: error text
        """
        # get class name
        module  = self.__class__.__name__
        tmpStr  = '{0}: Error: {1}'.format(module, msg)
        print('\n' + '!' * 30 + '   ERROR   ' + '!' * 30)
        print(tmpStr)

    def warning(self, msg):
        """ Prints a warning
        :param msg: warning text
        :return: None
        """
        # get class name
        module  = self.__class__.__name__
        tmpStr  = '{0}: Warning: {1}'.format(module, msg)
        print(tmpStr)

    def cleanPath(self, path):
        """ Clean a path from special characters
        :param path: file path
        :return: cleaned file path
        """
        path = path.lower()
        # clean path
        for search in self.options['pathrepl'] :
            path = path.replace(str(search), str(self.options['pathrepl'][search]))

        return path

    def cleanFileName(self, filename):
        """ Clean a filename from special characters
        :param filename: file name to clean
        :return: cleaned file name
        """
        filename = filename.lower()
        # clean path
        for search in self.options['pathrepl'] :
            filename = filename.replace(str(search), str(self.options['pathrepl'][search]))

        return filename
