""" Example to use table writers
"""

import plotscripts.data
import plotscripts.table

print('I am alive')

inputArg = plotscripts.InputArgs()
inputArg.setOption('debug', True)
inputArg.setOption('tabledir', 'tables')

# set data
inputArg.setData(plotscripts.data.TestData)

# get an index object
index = plotscripts.data.TestData.index()
index.calcType = 'num'
index.num = 1
index.min = 0

# create a table
table = inputArg.addTable('test', plotscripts.table.TxtTableWriter)
table.title = 'Test Table'

# add a row
row = table.addRow('first row')
row.setIndex(index)

# add a second row
index.min = 2
row = table.addRow('My 2nd')
row.setIndex(index)

# create bigger table
table = inputArg.addTable('test_big', plotscripts.table.LatexTableWriter)
table.title = 'Big test table'
table.ndim = 1  # can handle big data

index = plotscripts.data.TestData.index()
index.calcType = 'num'
index.num = 10
index.min = 0
index.step = 1

row = table.addRow('First')
row.setIndex(index)

index.step = 2
row = table.addRow('Second')
row.setIndex(index)

# run input
inputArg.run()

print('done')
