from WMCore.Configuration import Configuration
config = Configuration()

#Nj='1000'
#Nepj='5000'
#switch='2'
#cent='0-02'
#deltaEtaCut='2.0'

config.section_("General")

config.General.Nj='6'
config.General.Nepj='80'
config.General.switch='2'
config.General.cent='0-02'
config.General.deltaEtaCut='2.0'

argv = [config.General.Nj, config.General.Nepj, config.General.switch, config.General.cent, config.General.deltaEtaCut]
#print argv

#config.section_("General")
#config.General.requestName = 'HYDJET_'+...
config.General.workArea = 'crab_projects'

#argv = [config.General.Nj, config.General.Nepj, config.General.switch, config.General.cent, config.General.deltaEtaCut]
#print argv

config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
#config.JobType.psetName = 'testHydjet_new_crab.py'
config.JobType.psetName = 'pset.py'
config.JobType.scriptExe = 'job_new.sh'
#config.JobType.scriptArgs = argv[1:len(argv)]
config.JobType.scriptArgs = ['Nevt='+argv[1], 's='+argv[2], 'c='+argv[3], 'deltaEtaCut='+argv[4]]
#config.JobType.scriptArgs = [x for x in config.JobType.scriptArgs.split(',')][1:len(config.JobType.scriptArgs)]
#config.JobType.scriptArgs = [x for x in config.JobType.scriptArgs.split(',')]
#config.JobType.inputFiles = ['TrackCorrections_HYDJET_5320_hiGenPixelTrk_cent1030.root']
config.JobType.inputFiles = ['subjob_new.sh', 'testHydjet_new_crab.py']
config.JobType.disableAutomaticOutputCollection = True
#config.JobType.pyCfgParams = argv[1:len(argv)]
config.JobType.outputFiles = [ 'output_'+'_'.join(argv[1:len(argv)])+'.root' ]
#config.JobType.outputFiles = [ 'output_'+'_'.join(config.JobType.scriptArgs)+'.root' ]
config.JobType.sendPythonFolder = True
config.JobType.numCores = 8
config.JobType.maxMemoryMB = 3000
#config.JobType.maxMemoryMB = 2500

config.section_("Data")
config.Data.publication = False
config.Data.splitting = 'EventBased'
config.Data.totalUnits = int(config.General.Nj)
config.Data.unitsPerJob = 1
config.Data.ignoreLocality = True

config.section_("Site")
config.Site.storageSite = 'T2_US_MIT'

