from WMCore.Configuration import Configuration
config = Configuration()

argv = ['5', '10', '2', '50-60', '2.0']

config.section_("General")
#config.General.requestName = 'HYDJET_'+...
config.General.workArea = 'crab_projects'

config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'testHydjet_new_crab.py'
#config.JobType.inputFiles = ['TrackCorrections_HYDJET_5320_hiGenPixelTrk_cent1030.root']
config.JobType.disableAutomaticOutputCollection = True
config.JobType.pyCfgParams = argv[1:len(argv)]
config.JobType.outputFiles = [ 'output_'+'_'.join(argv[1:len(argv)])+'.root' ]

config.section_("Data")
config.Data.outputPrimaryDataset = 'MinBias'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = int(argv[1])
Njobs = int(argv[0])
config.Data.totalUnits = Njobs * config.Data.unitsPerJob
config.Data.publishDBS = 'phys03'
config.Data.outputDatasetTag = 'HYDJET_generation_test'

config.section_("Site")
config.Site.storageSite = 'T2_US_MIT'
