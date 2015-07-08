'''
Created on Aug 29, 2013

@author: Hans R Hammer
statistic stest file
'''

import plotscripts.data.testdata
import plotscripts.plotter.matplotlib.lineplotter

print('I am alive')

# create object
inputArg = plotscripts.InputArgs()
# set a few options, will be passed to sub objects
# this options are global, options also can be set in the sub objects
inputArg._options['debug'] = True
inputArg._options['plotdir'] = 'plot/data/'

# create test data executioner
inputArg._data = plotscripts.data.testdata.TestData()

# create some statistics, create sum, mean, stdDeviation, meanMax|Min = mean +- stdDeviation
# the input is the same as for the plots
# the name is later used to get the data from the statistic
# weights correspond to number of inputs above (e.g. 3 here), the default if not given is 1/N
# the columns are for which variables the statistic should be prepared
# the input list is prepared in advance
inputList = []
wheights = []
for idx in range(20):
   inputList.append(['rnd', 10])
   wheights.append(1.0/(idx + 1))
   
# create statistics
statistic = inputArg._data.Statistic()
statistic.input    = inputList
statistic.columns  = ['column']
statistic.wheights = wheights
statistic.method   = 'value'
statistic.basedata = None
inputArg._data.statistics['test'] = statistic

# plot statistic in a line plot
# the factor for avgMax/Min can be given as third parameter
inputArg._plots['statistic'] = plotscripts.plotter.matplotlib.lineplotter.LinePlotter()

for data in [['test', 'avg'], ['test', 'avgMax', 1], ['test', 'avgMin', 0.5], ['test', 'max']]:
   line = inputArg._plots['statistic'].Line()
   line.data = data
   line.title = data[1]
   inputArg._plots['statistic'].input.append(line)
   
inputArg._plots['statistic'].xValues  = list(range(10))
inputArg._plots['statistic'].columns   = ['column']

#run the stuff
inputArg.run()
print('done')