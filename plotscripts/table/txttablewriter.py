""" Table writer for text files
"""

from plotscripts.table.basetablewriter import BaseTableWriter


class TxtTableWriter(BaseTableWriter):
    def __init__(self, name):
        """ Constructor
        """
        super().__init__(name)

    def writeTable(self, path, filename, tableData):
        """
        Base method for writing the prepared table to a file
        """
        with open(path + '/' + filename + '.tab', 'w') as tableFile:
            for row in tableData:
                tmpStr = ''
                for column in row:
                    tmpStr += '{0}{1}'.format(column, self._getOption('separator'))

                tableFile.write(tmpStr + '\n')
