""" Table writer for latex files
"""

from plotscripts.table.basetablewriter import BaseTableWriter


class LatexTableWriter(BaseTableWriter):
    def __init__(self, name):
        """ Constructor
        """
        super().__init__(name)

    def writeTable(self, path, filename, tableData):
        """
        Base method for writing the prepared table to a file
        """
        with open(path + '/' + filename + '.tex', 'w') as tableFile:
            colStr = 'c' * len(tableData[0])

            tableFile.write('\\begin{table}\n')
            tableFile.write('\t\\caption{{0}}\n'.format(self.title))
            tableFile.write('\t\\label{{tab:{0}}}\n'.format(self._name))

            tableFile.write('\t\\begin{{tabular}}{{{0}}}\n'.format(colStr))

            for row in tableData:
                tmpStr = '\t\t{0}'.format(row[0])
                for column in row[1:]:
                    tmpStr += '\t&\t{0}'.format(column)

                tableFile.write(tmpStr + '\t\\\\\n')

            tableFile.write('\t\\end{tabular}\n')
            tableFile.write('\\end{table}\n')
