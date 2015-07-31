"""
Created on Apr 26, 2013

@author: Hans R Hammer

Provides a base object for all modules.
All used modules must inherit from this class
"""

from plotscripts.base.exception import PlotscriptException as _PlotscriptException

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

    class Option:
        """ Container class for an option

        :var name:
        :var value:
        :var description:
        :var visibility: private, down, up, global
        """

        def __init__(self, name, value, description='', visibility='private'):
            """ Contructor
            :param name:
            :param value:
            :param description:
            :param visibility:
            :return:
            """
            self.name = name
            self.value = value
            self.description = description
            self.visibility = visibility

    debugging = False
    Exception = _PlotscriptException

    def __init__(self):
        """ Constructor """
        self._options = {}  # dict for user set options
        self._defaults = {}  # dict for default options

        self._addDefault('debug', False, 'Turn on debug mode')
        self._addDefault('pathrepl', {'.': '', ' ': '_', '//': '/', '-': '_'},
                         'Characters replaces in file names and paths')

    def setOption(self, name, value, visibility=None, description=None):
        """ set option in the object
        :param name: name of the option
        :param value:
        :param visibility:
        :param description:
        :return:
        """
        if name in self._defaults:
            if visibility is None:
                visibility = self._defaults[name].visibility
            if description is None:
                description = self._defaults[name].description
        else:
            if visibility is None:
                visibility = 'down'
        self._options[name] = self.Option(name, value, description, visibility)

    def _getOption(self, name):
        """ Retrieve the value of an options

        :param name: name of option
        :return: value of option
        """
        if name not in self._options:
            raise self._exception('{0} is not an available option'.format(name))
        return self._options[name].value

    def copyOptions(self, options):
        """
        Setting options in object without overwriting existing ones
        :param options: options to set in this object
        """
        for key, option in options.items():
            if key not in self._options.keys() \
                    and (option.visibility == 'down' or option.visibility == 'global'):
                self._options[key] = option

    def getOptions(self):
        """
        getting options from an object without overwriting
        """
        return self._options

    def _retrieveOptions(self, pObject):
        """ Retrieves options from a subobject
        :return: None
        """
        if not issubclass(pObject.__class__, BaseObject):
            raise self._exception('{0} is not a valid module'.format(pObject.__class__.__name__))

        options = pObject.getOptions()
        for key, option in options.items():
            if key not in self._options \
                    and option.visibility == 'up' or option.visibility == 'global':
                self._options[key] = option

    def _addDefault(self, name, value, description='', visibility='private'):
        """ add default option to class

        :param name: name of the option
        :param value: default value of the option
        :param description: short description
        :return: None
        """
        self._defaults[name] = self.Option(name, value, description, visibility)

    def _activateDefaults(self):
        """ set missing options to defaults """
        # setting remaining defaults
        for option in self._defaults:
            if option not in self._options:
                self._options[option] = self._defaults[option]

    def printOptions(self):
        """ print all available options
        :return: None
        """
        self._out('Available options')
        for name, option in sorted(self._defaults.items()):
            self._out('{0} - {1}, default {2}, {3}'.format(option.name, option.description,
                                                           option.value, option.visibility))

    def _checkInput(self):
        """ Check the provided input
        :return: None
        """
        pass

    def _exception(self, msg):
        """
        Creates and return an exception
        @param msg: message text for exception
        @return: exception
        """
        # get class name
        module = self.__class__.__name__
        # get function name
        function = inspect.stack()[1][3]
        # create exception
        return self.Exception(module, function, msg)

    def _out(self, msg):
        """
        Prints a message
        :param msg: message text
        """
        # get class name
        module = self.__class__.__name__
        tmpStr = '{0}: {1}'.format(module, msg)
        print(tmpStr)

    def _debug(self, msg):
        """
        Prints a debbuging message, only if option debug is set
        :param msg: message text
        """
        if self.debugging or self._getOption('debug'):
            # get class name
            module = self.__class__.__name__
            tmpStr = '{0}: {1}'.format(module, msg)
            print(tmpStr)

    def _error(self, msg):
        """
        prints an error msg
        :param msg: error text
        """
        # get class name
        module = self.__class__.__name__
        tmpStr = '{0}: Error: {1}'.format(module, msg)
        print('\n' + '!' * 30 + '   ERROR   ' + '!' * 30)
        print(tmpStr)

    def _warning(self, msg):
        """ Prints a warning
        :param msg: warning text
        :return: None
        """
        # get class name
        module = self.__class__.__name__
        tmpStr = '{0}: Warning: {1}'.format(module, msg)
        print(tmpStr)

    def _cleanPath(self, path):
        """ Clean a path from special characters
        :param path: file path
        :return: cleaned file path
        """
        path = path.lower()
        # clean path
        for search in self._getOption('pathrepl'):
            path = path.replace(str(search), str(self._getOption('pathrepl')[search]))

        return path

    def _cleanFileName(self, filename):
        """ Clean a filename from special characters
        :param filename: file name to clean
        :return: cleaned file name
        """
        filename = filename.lower()
        # clean path
        for search in self._getOption('pathrepl'):
            filename = filename.replace(str(search), str(self._getOption('pathrepl')[search]))

        return filename
