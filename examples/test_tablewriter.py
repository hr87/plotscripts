'''
Created on Jul 22, 2013

@author: hammhr
'''

import plotscripts.data.xsdata
import plotscripts.table.basetablewriter

print('I am alive')
inputArg = plotscripts.InputArgs()
inputArg._options['debug'] = True
inputArg._options['tabledir'] = 'tables'

# set options
inputArg._options['style']   = ['g', 'm']
inputArg._options['xScale']  = 'log'

# set data
inputArg._data = plotscripts.data.xsdata.XsData()
inputArg._data.file['test']      = 'data/block_80.xs'
inputArg._data.groupStructure    = [ 20.000E+00, 7.4082E+00, 3.6788E+00, 6.3928E-01, 1.1109E-01, 1.9305E-02,
                                    3.3546E-03, 1.5846E-03, 7.4852E-04, 2.7537E-04, 1.3007E-04, 7.5281E-05, 
                                    2.7550E-05, 1.3550E-05, 8.3000E-06, 5.1100E-06, 2.3300E-06, 1.3079E-06, 
                                    6.7000E-07, 3.5767E-07, 1.8443E-07, 1.1157E-07, 8.1968E-08, 5.0000E-08, 
                                    2.0492E-08, 1.2396E-08, 1.00E-10 ]

# create a plot    
inputArg._tables['xs'] = plotscripts.table.basetablewriter.BaseTableWriter()
inputArg._tables['xs'].input     = [ ['test', 1, 1], ['test', 3, 1]]
inputArg._tables['xs'].columns    = ['flux_norm', ['flux_norm', 'rel']]
inputArg._tables['xs'].basedata  = ['test', 1, 1]
inputArg._tables['xs'].ndim = 0

# create a plot    
inputArg._tables['xs1'] = plotscripts.table.basetablewriter.BaseTableWriter()
inputArg._tables['xs1'].input     = [ ['test', 1, None], ['test', 3, None]]
inputArg._tables['xs1'].columns    = ['flux_norm', ['flux_norm', 'rel']]
inputArg._tables['xs1'].basedata  = ['test', 1, None]
inputArg._tables['xs1'].ndim = 1


# run input
inputArg.run()

print('done')
