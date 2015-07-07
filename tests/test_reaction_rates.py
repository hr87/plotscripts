'''
Created on Jun 18, 2013

@author: hammhr
'''

import plotscripts.data.reactionrates
import plotscripts.plotter.svg.mapplotter
import plotscripts.geometry.vhtrc.triangular
#import compare.plotter.matplotlib.base2dplotter

print('I am alive')
inputArg = plotscripts.InputArgs()
inputArg.options['plotdir'] = 'plot/' 
inputArg.options['sameLvls'] = False

# set options
inputArg.options['style']   = ['g', 'm']
inputArg.options['xScale']  = 'log'
inputArg.options['debug']   = True

# set data
inputArg.data = plotscripts.data.reactionrates.ReactionRate()
inputArg.data.files['xs']           = inputArg.data.File()
inputArg.data.files['xs'].fileName  = 'data/block_80.xs'
inputArg.data.files['xs'].type      = 'xs'

inputArg.data.files['flux']          = inputArg.data.File()
inputArg.data.files['flux'].fileName = 'data/block_80.flux'
inputArg.data.files['flux'].type     = 'flux'
inputArg.data.files['flux'].xsFile   = 'xs'
inputArg.data.files['flux'].xsMapping= [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
inputArg.data.files['flux'].volumes  = [0.5] * 384 + [0.72 ] * 384 + [0.475] * 384

inputArg.data.files['pwr']           = inputArg.data.File()
inputArg.data.files['pwr'].fileName  = 'data/hp_255_block_d.pwr'
inputArg.data.files['pwr'].type      = 'pwr'
inputArg.data.files['pwr'].xsFile    = 'xs'
inputArg.data.files['pwr'].xsMapping = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 3, 3, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
inputArg.data.files['pwr'].volumes   = [0.5] * 384 + [0.72 ] * 384 + [0.475] * 384


inputArg.data.groupStructure    = [ 20.000E+00, 7.4082E+00, 3.6788E+00, 6.3928E-01, 1.1109E-01, 1.9305E-02,          
                                    3.3546E-03, 1.5846E-03, 7.4852E-04, 2.7537E-04, 1.3007E-04, 7.5281E-05, 
                                    2.7550E-05, 1.3550E-05, 8.3000E-06, 5.1100E-06, 2.3300E-06, 1.3079E-06, 
                                    6.7000E-07, 3.5767E-07, 1.8443E-07, 1.1157E-07, 8.1968E-08, 5.0000E-08, 
                                    2.0492E-08, 1.2396E-08, 1.00E-10 ]
blocks = [1000, 1001, 1002, 1003, 1004, 1005, 1010, 1011, 1012, 1013, 1014, 1015, 1020, 1021, 1022, 1023, 1024, 1025, 1030, 1031, 1032, 1033, 1034, 1035, 1040, 1041, 1042, 1043, 1044, 1045, 1050, 1051, 1052, 1053, 1054, 1055, 1060, 1061, 1062, 1063, 1064, 1065, 1070, 1071, 1072, 1073, 1074, 1075, 1080, 1081, 1082, 1083, 1084, 1085, 1090, 1091, 1092, 1093, 1094, 1095, 1100, 1101, 1102, 1103, 1104, 1105, 1110, 1111, 1112, 1113, 1114, 1115, 1120, 1121, 1122, 1123, 1124, 1125, 1130, 1131, 1132, 1133, 1134, 1135, 1140, 1141, 1142, 1143, 1144, 1145, 1150, 1151, 1152, 1153, 1154, 1155, 1160, 1161, 1162, 1163, 1164, 1165, 1170, 1171, 1172, 1173, 1174, 1175, 1180, 1181, 1182, 1183, 1184, 1185, 1190, 1191, 1192, 1193, 1194, 1195, 1200, 1201, 1202, 1203, 1204, 1205, 1210, 1211, 1212, 1213, 1214, 1215, 1220, 1221, 1222, 1223, 1224, 1225, 1230, 1231, 1232, 1233, 1234, 1235, 1240, 1241, 1242, 1243, 1244, 1245, 1250, 1251, 1252, 1253, 1254, 1255, 1260, 1261, 1262, 1263, 1264, 1265, 1270, 1271, 1272, 1273, 1274, 1275, 1280, 1281, 1282, 1283, 1284, 1285, 1290, 1291, 1292, 1293, 1294, 1295, 1300, 1301, 1302, 1303, 1304, 1305, 1310, 1311, 1312, 1313, 1314, 1315, 1320, 1321, 1322, 1323, 1324, 1325, 1330, 1331, 1332, 1333, 1334, 1335, 1340, 1341, 1342, 1343, 1344, 1345, 1350, 1351, 1352, 1353, 1354, 1355, 1360, 1361, 1362, 1363, 1364, 1365, 1370, 1371, 1372, 1380, 1381, 1382, 1383, 1384, 1385, 1390, 1391, 1392, 1393, 1394, 1395, 1400, 1401, 1402, 1403, 1404, 1405, 1410, 1411, 1412, 1420, 1421, 1422, 1423, 1424, 1425, 1430, 1431, 1432, 1433, 1434, 1435, 1440, 1441, 1442, 1443, 1444, 1445, 1450, 1451, 1452, 1460, 1461, 1462, 1463, 1464, 1465, 1470, 1471, 1472, 1473, 1474, 1475, 1480, 1481, 1482, 1483, 1484, 1485, 1490, 1491, 1492, 1500, 1501, 1502, 1503, 1504, 1505, 1510, 1511, 1512, 1513, 1514, 1515, 1520, 1521, 1522, 1523, 1524, 1525, 1530, 1531, 1532, 1540, 1541, 1542, 1543, 1544, 1545, 1550, 1551, 1552, 1553, 1554, 1555, 1560, 1561, 1562, 1563, 1564, 1565, 1570, 1571, 1572, 1580, 1581, 1582, 1583, 1584, 1585, 1590, 1591, 1592, 1593, 1594, 1595, 1600, 1601, 1602, 1603, 1604, 1605, 1610, 1611, 1612, 1620, 1621, 1622, 1630, 1631, 1632, 1640, 1641, 1642, 1650, 1651, 1652, 1660, 1661, 1662, 1670, 1671, 1672, 1680, 1681, 1682, 1690, 1691, 1692, 1700, 1701, 1702, 1710, 1711, 1712, 1720, 1721, 1722, 2000, 2001, 2002, 2003, 2004, 2005, 2010, 2011, 2012, 2013, 2014, 2015, 2020, 2021, 2022, 2023, 2024, 2025, 2030, 2031, 2032, 2033, 2034, 2035, 2040, 2041, 2042, 2043, 2044, 2045, 2050, 2051, 2052, 2053, 2054, 2055, 2060, 2061, 2062, 2063, 2064, 2065, 2070, 2071, 2072, 2073, 2074, 2075, 2080, 2081, 2082, 2083, 2084, 2085, 2090, 2091, 2092, 2093, 2094, 2095, 2100, 2101, 2102, 2103, 2104, 2105, 2110, 2111, 2112, 2113, 2114, 2115, 2120, 2121, 2122, 2123, 2124, 2125, 2130, 2131, 2132, 2133, 2134, 2135, 2140, 2141, 2142, 2143, 2144, 2145, 2150, 2151, 2152, 2153, 2154, 2155, 2160, 2161, 2162, 2163, 2164, 2165, 2170, 2171, 2172, 2173, 2174, 2175, 2180, 2181, 2182, 2183, 2184, 2185, 2190, 2191, 2192, 2193, 2194, 2195, 2200, 2201, 2202, 2203, 2204, 2205, 2210, 2211, 2212, 2213, 2214, 2215, 2220, 2221, 2222, 2223, 2224, 2225, 2230, 2231, 2232, 2233, 2234, 2235, 2240, 2241, 2242, 2243, 2244, 2245, 2250, 2251, 2252, 2253, 2254, 2255, 2260, 2261, 2262, 2263, 2264, 2265, 2270, 2271, 2272, 2273, 2274, 2275, 2280, 2281, 2282, 2283, 2284, 2285, 2290, 2291, 2292, 2293, 2294, 2295, 2300, 2301, 2302, 2303, 2304, 2305, 2310, 2311, 2312, 2313, 2314, 2315, 2320, 2321, 2322, 2323, 2324, 2325, 2330, 2331, 2332, 2333, 2334, 2335, 2340, 2341, 2342, 2343, 2344, 2345, 2350, 2351, 2352, 2353, 2354, 2355, 2360, 2361, 2362, 2363, 2364, 2365, 2370, 2371, 2372, 2380, 2381, 2382, 2383, 2384, 2385, 2390, 2391, 2392, 2393, 2394, 2395, 2400, 2401, 2402, 2403, 2404, 2405, 2410, 2411, 2412, 2420, 2421, 2422, 2423, 2424, 2425, 2430, 2431, 2432, 2433, 2434, 2435, 2440, 2441, 2442, 2443, 2444, 2445, 2450, 2451, 2452, 2460, 2461, 2462, 2463, 2464, 2465, 2470, 2471, 2472, 2473, 2474, 2475, 2480, 2481, 2482, 2483, 2484, 2485, 2490, 2491, 2492, 2500, 2501, 2502, 2503, 2504, 2505, 2510, 2511, 2512, 2513, 2514, 2515, 2520, 2521, 2522, 2523, 2524, 2525, 2530, 2531, 2532, 2540, 2541, 2542, 2543, 2544, 2545, 2550, 2551, 2552, 2553, 2554, 2555, 2560, 2561, 2562, 2563, 2564, 2565, 2570, 2571, 2572, 2580, 2581, 2582, 2583, 2584, 2585, 2590, 2591, 2592, 2593, 2594, 2595, 2600, 2601, 2602, 2603, 2604, 2605, 2610, 2611, 2612, 2620, 2621, 2622, 2630, 2631, 2632, 2640, 2641, 2642, 2650, 2651, 2652, 2660, 2661, 2662, 2670, 2671, 2672, 2680, 2681, 2682, 2690, 2691, 2692, 2700, 2701, 2702, 2710, 2711, 2712, 2720, 2721, 2722, 3000, 3001, 3002, 3003, 3004, 3005, 3010, 3011, 3012, 3013, 3014, 3015, 3020, 3021, 3022, 3023, 3024, 3025, 3030, 3031, 3032, 3033, 3034, 3035, 3040, 3041, 3042, 3043, 3044, 3045, 3050, 3051, 3052, 3053, 3054, 3055, 3060, 3061, 3062, 3063, 3064, 3065, 3070, 3071, 3072, 3073, 3074, 3075, 3080, 3081, 3082, 3083, 3084, 3085, 3090, 3091, 3092, 3093, 3094, 3095, 3100, 3101, 3102, 3103, 3104, 3105, 3110, 3111, 3112, 3113, 3114, 3115, 3120, 3121, 3122, 3123, 3124, 3125, 3130, 3131, 3132, 3133, 3134, 3135, 3140, 3141, 3142, 3143, 3144, 3145, 3150, 3151, 3152, 3153, 3154, 3155, 3160, 3161, 3162, 3163, 3164, 3165, 3170, 3171, 3172, 3173, 3174, 3175, 3180, 3181, 3182, 3183, 3184, 3185, 3190, 3191, 3192, 3193, 3194, 3195, 3200, 3201, 3202, 3203, 3204, 3205, 3210, 3211, 3212, 3213, 3214, 3215, 3220, 3221, 3222, 3223, 3224, 3225, 3230, 3231, 3232, 3233, 3234, 3235, 3240, 3241, 3242, 3243, 3244, 3245, 3250, 3251, 3252, 3253, 3254, 3255, 3260, 3261, 3262, 3263, 3264, 3265, 3270, 3271, 3272, 3273, 3274, 3275, 3280, 3281, 3282, 3283, 3284, 3285, 3290, 3291, 3292, 3293, 3294, 3295, 3300, 3301, 3302, 3303, 3304, 3305, 3310, 3311, 3312, 3313, 3314, 3315, 3320, 3321, 3322, 3323, 3324, 3325, 3330, 3331, 3332, 3333, 3334, 3335, 3340, 3341, 3342, 3343, 3344, 3345, 3350, 3351, 3352, 3353, 3354, 3355, 3360, 3361, 3362, 3363, 3364, 3365, 3370, 3371, 3372, 3380, 3381, 3382, 3383, 3384, 3385, 3390, 3391, 3392, 3393, 3394, 3395, 3400, 3401, 3402, 3403, 3404, 3405, 3410, 3411, 3412, 3420, 3421, 3422, 3423, 3424, 3425, 3430, 3431, 3432, 3433, 3434, 3435, 3440, 3441, 3442, 3443, 3444, 3445, 3450, 3451, 3452, 3460, 3461, 3462, 3463, 3464, 3465, 3470, 3471, 3472, 3473, 3474, 3475, 3480, 3481, 3482, 3483, 3484, 3485, 3490, 3491, 3492, 3500, 3501, 3502, 3503, 3504, 3505, 3510, 3511, 3512, 3513, 3514, 3515, 3520, 3521, 3522, 3523, 3524, 3525, 3530, 3531, 3532, 3540, 3541, 3542, 3543, 3544, 3545, 3550, 3551, 3552, 3553, 3554, 3555, 3560, 3561, 3562, 3563, 3564, 3565, 3570, 3571, 3572, 3580, 3581, 3582, 3583, 3584, 3585, 3590, 3591, 3592, 3593, 3594, 3595, 3600, 3601, 3602, 3603, 3604, 3605, 3610, 3611, 3612, 3620, 3621, 3622, 3630, 3631, 3632, 3640, 3641, 3642, 3650, 3651, 3652, 3660, 3661, 3662, 3670, 3671, 3672, 3680, 3681, 3682, 3690, 3691, 3692, 3700, 3701, 3702, 3710, 3711, 3712, 3720, 3721, 3722]
layer2 = [blocks[idx] for idx in range(384,768)]

# create a plot    
inputArg.plot['reaction_rate'] = plotscripts.plotter.svg.mapplotter.MapPlotter()
inputArg.plot['reaction_rate'].geometry  = plotscripts.geometry.vhtrc.triangular.VHTRCTriangular()
inputArg.plot['reaction_rate'].input     = [ ['flux', layer2], ['pwr', layer2]]
inputArg.plot['reaction_rate'].columns   = ['flux', 'fission_rate']
inputArg.plot['reaction_rate'].method    = ['value']
inputArg.plot['reaction_rate'].basedata  = ['flux', layer2]

# run input
inputArg.run()

print('done')
