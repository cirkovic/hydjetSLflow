from WMCore.Configuration import Configuration
config = Configuration()

#argv = ['5', '64', '2', '50-60', '2.0']
argv = ['1', '42', '2', '50-60', '2.0']

config.section_("General")
#config.General.requestName = 'HYDJET_'+...
config.General.workArea = 'crab_projects'

config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
#config.JobType.psetName = 'testHydjet_new_crab.py'
config.JobType.psetName = 'pset.py'
config.JobType.scriptExe = 'job_new.sh'
#config.JobType.scriptArgs = argv[1:len(argv)]
config.JobType.scriptArgs = ['Nevt='+argv[1], 's='+argv[2], 'c='+argv[3], 'deltaEtaCut='+argv[4]]
#config.JobType.inputFiles = ['TrackCorrections_HYDJET_5320_hiGenPixelTrk_cent1030.root']
config.JobType.inputFiles = ['subjob_new.sh', 'testHydjet_new_crab.py']
config.JobType.disableAutomaticOutputCollection = True
#config.JobType.pyCfgParams = argv[1:len(argv)]
config.JobType.outputFiles = [ 'output_'+'_'.join(argv[1:len(argv)])+'.root' ]
config.JobType.sendPythonFolder = True

config.section_("Data")
config.Data.publication = False
config.Data.splitting = 'EventBased'
config.Data.totalUnits = int(argv[0])
config.Data.unitsPerJob = 1
config.Data.ignoreLocality = True

config.section_("Site")
config.Site.storageSite = 'T2_US_MIT'
