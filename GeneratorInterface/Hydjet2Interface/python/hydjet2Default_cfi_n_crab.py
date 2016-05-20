import FWCore.ParameterSet.Config as cms
source = cms.Source("EmptySource")
from GeneratorInterface.Hydjet2Interface.hydjet2DefaultParameters_cff import *

from GeneratorInterface.Hydjet2Interface.offset import *

centd = {
    #'0-0'   : (  0.0,          0.324481317 ), # 0.324868055
    '0-02'  : (  0.0,          0.324481317 ), # 0.324868055
    '0-05'  : (  0.0,          0.727564543 ), # 0.72775505
    '0-5'   : (  0.0,          3.475007888 ),
    '5-6'   : (  3.475007888,  3.883832345 ),
    '6-10'  : (  3.883832345,  5.042168308 ),
    '10-12' : (  5.042168308,  5.519130175 ),
    '12-15' : (  5.519130175,  6.200504271 ),
    '15-20' : (  6.200504271,  7.154428005 ),
    '20-25' : (  7.154428005,  8.040214329 ),
    '25-30' : (  8.040214329,  8.789725835 ),
    '30-35' : (  8.789725835,  9.47109993  ),
    '35-40' : (  9.47109993,  10.15247403  ),
    '40-45' : ( 10.15247403,  10.76571071  ),
    '45-50' : ( 10.76571071,  11.3789474   ),
    '50-55' : ( 11.3789474,   11.92404667  ),
    '55-60' : ( 11.92404667,  12.46914595  ),
    '60-65' : ( 12.46914595,  12.94610782  ),
    '65-70' : ( 12.94610782,  13.42306969  ),
    '70-75' : ( 13.42306969,  14.03630637  ),
    "0-5"   : (  0.0,          3.475007888 ),
    "5-10"  : (  3.475007888,  5.042168308 ),
    "0-10"  : (  0.0,          5.042168308 ),
    "10-20" : (  5.042168308,  7.154428005 ),
    "20-30" : (  7.154428005, 8.789725835  ),
    "30-40" : (  8.789725835, 10.15247403  ),
    "40-50" : (  10.15247403, 11.3789474   ),
    "50-60" : ( 11.3789474,   12.46914595  ),
}

generator = cms.EDFilter("Hydjet2GeneratorFilter",
	#collisionParameters5100GeV,
    collisionParameters2760GeV,
	qgpParameters,
	hydjet2Parameters,
	fNhsel 	= cms.int32(int(argv[ISWTC])), 	# Flag to include jet (J)/jet quenching (JQ) and hydro (H) state production, fNhsel (0 H on & J off, 1 H/J on & JQ off, 2 H/J/HQ on, 3 J on & H/JQ off, 4 H off & J/JQ on)
	PythiaParameters = cms.PSet(PythiaDefaultBlock,
		parameterSets = cms.vstring(
			#'pythiaUESettings',
			'hydjet2PythiaDefault',
			'ProQ2Otune',
			#'pythiaJets',
			#'pythiaPromptPhotons'

			#'myParameters',
			#'pythiaZjets',
			#'pythiaBottomoniumNRQCD',
			#'pythiaCharmoniumNRQCD',
			#'pythiaQuarkoniaSettings',
			#'pythiaWeakBosons'
		)
	),
	
	maxEventsToPrint = cms.untracked.int32(0),
	pythiaPylistVerbosity = cms.untracked.int32(0),

	fIfb 	= cms.int32(1), 	# Flag of type of centrality generation, fBfix (=0 is fixed by fBfix, >0 distributed [fBfmin, fBmax])
	#fBmin 	= cms.double(0.),	# Minimum impact parameter, fBmin
	#fBmax	= cms.double(3.47500770746), 	# Maximum impact parameter, fBmax
    fBmin   = cms.double(centd[argv[ICENT]][0]),   # Minimum impact parameter, fBmin
    fBmax   = cms.double(centd[argv[ICENT]][1]),    # Maximum impact parameter, fBmax
	fBfix 	= cms.double(0.), 	# Fixed impact parameter, fBfix

)
'''
RA(Pb) ~= 6.813740957 fm

% cent  	b/RA 
0           0          
0.2         0.04762161 # or 0.047678369
0.5         0.106779014 # or 0.106806974
5           0.51
6           0.57
10          0.74 
12          0.81
15          0.91
20	        1.05
25      	1.18 
30          1.29
35          1.39
40          1.49
45      	1.58
50      	1.67
55	        1.75  
60          1.83
65	        1.90
70	        1.97 
75	        2.06
'''
