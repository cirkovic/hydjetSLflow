from ROOT import *
from subprocess import call
import sys

#call(['cp', '-f', '30_40/out_30_40.root', 'out_30_40_test.root'])

centralities = ["00_05", "00_10", "10_20", "20_30", "30_40", "40_50", "50_60"]

fs = []

for cent in centralities:
    #fs.append(TFile.Open('30_40/out_30_40.root', 'UPDATE'))
    #fs.append(TFile.Open('out_30_40_test.root', 'UPDATE'))
    fs.append(TFile.Open(cent+'/out_'+cent+'.root', 'UPDATE'))
    f = fs[-1]

    cmbs = []
    for i in xrange(1, 8):
        for j in xrange(1, 8):
            if (i, j) not in cmbs and (j, i) not in cmbs:
                cmbs.append((i, j))

    '''
    arr = [
    ('PCA/General', ["trackhisto;1", "histo_vertex_z;1", "histo_vertex_x;1", "histo_vertex_y;1", "Mix;1"], '../..'),
    ('PCA/PT/30_40', ["P"+str(j)+"_30_40;1" for j in xrange(1, 8)], '../../..'),
    ('PCA/Q_VALUES/30_40/Correction_Sig', ["CORR_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../..'),
    ('PCA/Q_VALUES/30_40/Correction_Back', ["CORR_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../..'),
    ('PCA/Q_VALUES/30_40/Signal/n0/PAIRS_WITH_CUT', ["Pairs_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Signal/n0/PAIRS_WITH_CUT_EFF', ["Pairs_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Signal/n0/PAIRS_TOTAL', ["Pairs_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Signal/n0/PAIRS_TOTAL_EFF', ["Pairs_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Signal/n2/COS_NOT_NORMED_EFF', ["cosDelta_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Signal/n2/COS_NORMED_EFF', ["cosDelta_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Signal/n3/COS_NOT_NORMED_EFF', ["cosDelta_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Signal/n3/COS_NORMED_EFF', ["cosDelta_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Background/n0/PAIRS_WITH_CUT', ["Pairs_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Background/n0/PAIRS_WITH_CUT_EFF', ["Pairs_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Background/n0/PAIRS_TOTAL', ["Pairs_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Background/n0/PAIRS_TOTAL_EFF', ["Pairs_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Background/n2/COS_NOT_NORMED', ["cosDelta_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Background/n2/COS_NORMED', ["cosDelta_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Background/n2/COS_NOT_NORMED_EFF', ["cosDelta_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Background/n2/COS_NORMED_EFF', ["cosDelta_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Background/n3/COS_NOT_NORMED', ["cosDelta_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Background/n3/COS_NORMED', ["cosDelta_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Background/n3/COS_NOT_NORMED_EFF', ["cosDelta_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Background/n3/COS_NORMED_EFF', ["cosDelta_P"+str(i)+"P"+str(j)+";1" for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/30_40/Multiplicity_eff', ["P"+str(j)+"_multiplicity;1" for j in xrange(1, 8)], '../../../..'),
    ('PCA/Q_VALUES/30_40/Multiplicity_eff', ["P"+str(j)+"_multiplicity;1" for j in xrange(1, 8)], '../../../..'),
    ('PCA/Q_VALUES/30_40', ["pair_fraction_eff;1", "pair_fraction_back_eff;1", "tracks_count;1"], '../../..'),
    ]
    '''
    arr = [
    ('PCA/General', ['trackhisto;1', 'histo_vertex_z;1', 'histo_vertex_x;1', 'histo_vertex_y;1', 'Mix;1'], '../..'),
    ('PCA/PT/'+cent, ['P'+str(j)+'_'+cent+';1' for j in xrange(1, 8)], '../../..'),
    ('PCA/Q_VALUES/'+cent+'/Correction_Sig', ['CORR_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Correction_Back', ['CORR_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Signal/n0/PAIRS_WITH_CUT', ['Pairs_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Signal/n0/PAIRS_WITH_CUT_EFF', ['Pairs_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Signal/n0/PAIRS_TOTAL', ['Pairs_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Signal/n0/PAIRS_TOTAL_EFF', ['Pairs_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Signal/n2/COS_NOT_NORMED_EFF', ['cosDelta_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Signal/n2/COS_NORMED_EFF', ['cosDelta_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Signal/n3/COS_NOT_NORMED_EFF', ['cosDelta_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Signal/n3/COS_NORMED_EFF', ['cosDelta_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Background/n0/PAIRS_WITH_CUT', ['Pairs_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Background/n0/PAIRS_WITH_CUT_EFF', ['Pairs_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Background/n0/PAIRS_TOTAL', ['Pairs_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Background/n0/PAIRS_TOTAL_EFF', ['Pairs_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Background/n2/COS_NOT_NORMED', ['cosDelta_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Background/n2/COS_NORMED', ['cosDelta_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Background/n2/COS_NOT_NORMED_EFF', ['cosDelta_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Background/n2/COS_NORMED_EFF', ['cosDelta_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Background/n3/COS_NOT_NORMED', ['cosDelta_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Background/n3/COS_NORMED', ['cosDelta_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Background/n3/COS_NOT_NORMED_EFF', ['cosDelta_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Background/n3/COS_NORMED_EFF', ['cosDelta_P'+str(i)+'P'+str(j)+';1' for (i, j) in cmbs], '../../../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Multiplicity_eff', ['P'+str(j)+'_multiplicity;1' for j in xrange(1, 8)], '../../../..'),
    ('PCA/Q_VALUES/'+cent+'/Multiplicity_eff', ['P'+str(j)+'_multiplicity;1' for j in xrange(1, 8)], '../../../..'),
    ('PCA/Q_VALUES/'+cent+'', ['pair_fraction_eff;1', 'pair_fraction_back_eff;1', 'tracks_count;1'], '../../..'),
    ]

    for a in arr:
        #print a[0]
        gDirectory.cd(a[0])

        #gDirectory.ls()

        for i in a[1]:
            #print '\t',i
            gDirectory.Delete(i)

        #gDirectory.ls()

        gDirectory.cd(a[2])

    f.Close()
