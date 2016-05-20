from ROOT import *

fs = []
fs.append(TFile.Open('dcap://stormfe1.pi.infn.it:8444/gpfs/ddn/srm/cms/store/temp/user/cirkovic.7cd2552786a5886430723d90c1237104c1e2fb08/CRAB_PrivateMC/crab_20160714_102421/160714_082441/0000/output_2000_2_0-100_2.0_2.root'))
fs[-1].ls()

