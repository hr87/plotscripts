'''
Created on Aug 29, 2013

@author: Hans R Hammer
statistic stest file
'''

import plotscripts.data.testdata
import plotscripts.plotter.matplotlib

print('I am alive')

# create object
inputArg = plotscripts.InputArgs()
# set a few options, will be passed to sub objects
# this options are global, options also can be set in the sub objects
inputArg.setOption('debug', True)
inputArg.setOption('plotdir', '.')

# create test data executioner
data = inputArg.setData(plotscripts.data.TestData)

# create some statistics, create sum, mean, stdDeviation, meanMax|Min = mean +- stdDeviation
# the input is the same as for the plots
# the name is later used to get the data from the statistic
# weights correspond to number of inputs above (e.g. 3 here), the default if not given is 1/N
# the columns are for which variables the statistic should be prepared
# the input list is prepared in advance
stat = data.addStatistic('test')
for idx in range(100):
    index = data.index()
    index.calcType = 'rnd'
    index.num = 100
    index.min = 0
    index.max = 100
    stat.addInput(index)


inputList = []
wheights = []
for idx in range(20):
    inputList.append(['rnd', 10])
    wheights.append(1.0 / (idx + 1))

plot = inputArg.addPlot('statistic', plotscripts.plotter.matplotlib.LinePlotter)
plot.setOption('use_dirs', False)               # do not generate folder structure
plot.setOption('plotdir', './')                  # set folder to test folder
plot.setOption('format', 'png')                 # output format to png
plot.xValues = list(range(100))

# add lines for all statistic fields
for calc in [stat.Fields.avg, stat.Fields.min, stat.Fields.max,
             stat.Fields.avgMax, stat.Fields.avgMin]:
    line = plot.addLine(str(calc))

    index = data.statisticIndex()
    index.name = 'test'
    index.field = calc
    line.setIndex(index)


# run the stuff
inputArg.run()
print('done')
