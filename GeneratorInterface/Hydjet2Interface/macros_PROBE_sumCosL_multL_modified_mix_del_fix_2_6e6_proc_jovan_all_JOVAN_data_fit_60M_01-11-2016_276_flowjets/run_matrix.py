import sys, os
from subprocess import call
from modules import EigenData
import json
import itertools
import math
import random
import ROOT	
import operator
from sys import argv, exit
from ROOT import TF1
import numpy as np

OLD = True
GENMEAN = False
ACCOUNT_FIT = False

if ACCOUNT_FIT:
    PARSFILE='/afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src/GeneratorInterface/Hydjet2Interface/gaussian_fit_analyze/pars_best.json'
    with open(PARSFILE) as pars_file:
        pars = json.load(pars_file)

def GET_MATRIX(error_matrix, BINS):

  generated_matrix=dict()

  for bin in BINS:

       bin_value=error_matrix["dV_"+str(bin[0])+str(bin[1])]

       #random_error_value=random.uniform(-bin_value, bin_value)
       #random_error_value=np.random.normal(0, bin_value, 1)[0]
       random_error_value=np.random.normal(0, bin_value/3, 1)[0]

       generated_matrix["dV_"+str(bin[0])+str(bin[1])]=random_error_value

  return generated_matrix

#####################################

def SUM_MATRIX(matrix1, matrix2, BINS):

      sum_matrix=dict()

      for bin in BINS:

            temp_sum=matrix1["dV_"+str(bin[0])+str(bin[1])]+matrix2["V_"+str(bin[0])+str(bin[1])]
       
            sum_matrix["V_"+str(bin[0])+str(bin[1])]=temp_sum

      #print sum_matrix

      return sum_matrix
    

#####################################    

def GET_COMPONENT_VECTORS(vectors, DIM):

    WE=dict()
   

    for alpha in range(0, DIM):

        temp=[]

        for ei in range(1, DIM+1):


            #sub_temp=(vectors[(ei)][component].real, vectors[(ei)][component].imag)
            sub_temp=vectors[(ei)][alpha]
            temp.append(sub_temp)


        WE[str(alpha+1)]=temp

    return WE

#####################################

def GET_SIGN(current_vec, ref):

        REF=[]

          
        ####################### need complex format 
                                #to multiply with current_vec
        for i in ref:

            COM=complex(i, 0)
            REF.append(COM)

   

        unit=sum(map(operator.mul, REF, REF))
        prod=sum(map(operator.mul, current_vec, REF))

        temp=math.copysign(1, (prod/unit).real)

        return temp


######################################

def GET_TYPE(vector):

    type=0

    for x in vector:

         if x.imag!=0:

             type=1
             break

    return type

#######################################

def GET_REFERENCE_VECTORS(eigenvectors):

   WE=dict()

   for alpha in range(0, len(eigenvectors)):

        temp=[]

        for ei in range(1, len(eigenvectors)+1):

              sub_temp=eigenvectors[(ei)][alpha]
              temp.append(sub_temp)


        WE[str(alpha+1)]=temp


   return WE


#######################################

def main():

       ################################################
       # FILES
       ################################################

       try:

             working_folder=str(argv[1])
             ITER=str(argv[2])

       except:

             print "didn't import files!"
             exit()

       if ACCOUNT_FIT:
           #pars_data = open('/afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src/GeneratorInterface/Hydjet2Interface/test/gaussian_fit_new/pars_best.json')
           pars_data = open('/afs/cern.ch/work/c/cirkovic/hydjet/CMSSW_7_5_8_patch4/src/GeneratorInterface/Hydjet2Interface/gaussian_fit/pars_best.json')
           pars = json.load(pars_data)
           pars_data.close()

       cent = working_folder.split("/")[0]
       data_nx = working_folder.split("/")[2]
       nx = data_nx.split("_")[1]

       matrix_file=''
       matrix_error_file=''

       for filename in os.listdir(working_folder):
          if "Matrix" in filename:  
              matrix_file=working_folder+"/"+filename
              #print filename, "not error"

          if "Error" in filename: 
              matrix_error_file=working_folder+"/"+filename
              #print filename, "error"

       f1=open(matrix_file, "r")
       f2=open(matrix_error_file, "r")

       where_to_put=os.path.dirname(matrix_file)
      
       matrix=json.load(f1)  # CORRELATION MATRIX
       error_matrix=json.load(f2) # ERROR MATRIX

       DIM=int(math.sqrt(len(matrix)))

       fns = []
       if ACCOUNT_FIT:
           gfs = "[0]*exp(-((x-[1])^2)/(2*[2]^2))"
           gi = 0
           #gi = 1
           #gi = 3
           for i in range(0,DIM):
               fns.append(TF1("gf_"+str(i), gfs))
               #fns[-1].SetParameter(0, pars["2.76TeV_"+cent+"_"+nx+"_gfs_"+str(i)+"_mode_2"][0][3][0])
               fns[-1].SetParameter(0, 1.0)
               fns[-1].SetParameter(1, pars["2.76TeV_"+cent+"_"+nx+"_gfs_"+str(i)+"_mode_2"][0][gi][1])
               fns[-1].SetParameter(2, pars["2.76TeV_"+cent+"_"+nx+"_gfs_"+str(i)+"_mode_2"][0][gi][2])
               #fns[-1].Print()

       ENTRIES=int(ITER)
       #ENTRIES=1

       #################################################
       # SET REFERENCE VECTORS
       ##################################################

       clean_eigenvectors=dict()
       clean_eigenvalues=dict()

       EigenData( matrix, 1, DIM, clean_eigenvalues, clean_eigenvectors)  #DIM for entry

       #print "clean_eigenvectors=", clean_eigenvectors

       REF_VECTORS=GET_REFERENCE_VECTORS(clean_eigenvectors)  # regroup eigenvectors in sets that contain 
                                                              # the same component i from all eigenvectors
                                                              #did for initial (not perturbed) matrix
    
       f_clean_eigenvalues=open(where_to_put+"/clean_eigenvalues_"+str(DIM)+"x"+str(DIM)+".json", "w")
       f_clean_eigenvectors=open(where_to_put+"/clean_eigenvectors_"+str(DIM)+"x"+str(DIM)+".json", "w")

       json.dump(clean_eigenvalues, f_clean_eigenvalues, indent=2)
       json.dump(clean_eigenvectors, f_clean_eigenvectors, indent=2)


       ##################################################
       # Histograms
       ##################################################


       ROOT.gStyle.SetHistLineWidth(1);

       root_file = ROOT.TFile(where_to_put+"/pca_data.root", "recreate")
       sub_fol1 = root_file.mkdir("mode_1");
       root_file.cd("mode_1")

       pull_mode1 = ROOT.TH1F("lambda1","#lambda_{1}", 40000, 0, 2000)

       pull_mode1.GetXaxis().SetTitle("#lambda_{1}")
       pull_mode1.GetXaxis().SetTitleOffset(1.3)
       #pull_mode1.SetFillColor(39)
    
       ##################################################

       sub_fol2 = root_file.mkdir("mode_2");
       root_file.cd("mode_2")

       pull_mode2 = ROOT.TH1F("lambda2","#lambda_{2}", 30000, -10, 100)

       pull_mode2.GetXaxis().SetTitle("#lambda_{2}")
       pull_mode2.GetXaxis().SetTitleOffset(1.3)

       ###################################################

       ei_histo=[]
       ei_histo_1D=[]

       for i in range(0,DIM): 

            histo_name= "ei_histo_"+str(i)
            temp=ROOT.TH2F(histo_name,"pull distribution", 15, 0.5, 15.5, 30000, -1, 1)

            y_axis="e_{"+str(i+1)+"}"+"^"+"{#alpha}"         #x_{1}^{y}
            
            temp.GetYaxis().SetTitle(y_axis)
            temp.GetXaxis().SetTitle("#alpha")
            temp.GetXaxis().SetTitleOffset(1.2)
            temp.SetFillColor(39)

            ei_histo.append(temp)

       for i in range(0,DIM):

            histo_name= "ei_histo_1D"+str(i)
            temp=ROOT.TH1F(histo_name,"ei_histo_1D", 30000, -1, 1)

            y_axis="e_{"+str(i+1)+"}"+"^"+"{#alpha}"         #x_{1}^{y}

            temp.GetYaxis().SetTitle(y_axis)
            temp.GetXaxis().SetTitle("#alpha")
            temp.GetXaxis().SetTitleOffset(1.2)
            temp.SetFillColor(39)

            ei_histo_1D.append(temp)


       ##################################################

       sub_fol1 = root_file.mkdir("mode_3");
       root_file.cd("mode_3")

       pull_mode3 = ROOT.TH1F("lambda3","#lambda_{1}", 10000, -1.5, 50)

       pull_mode3.GetXaxis().SetTitle("#lambda_{3}")
       pull_mode3.GetXaxis().SetTitleOffset(1.3)
       #pull_mode3.SetFillColor(39)


       sub_fol1 = root_file.mkdir("mode_4");
       root_file.cd("mode_4")

       pull_mode4 = ROOT.TH1F("lambda4","#lambda_{4}", 5000, -1.5, 100)

       pull_mode4.GetXaxis().SetTitle("#lambda_{4}")
       pull_mode4.GetXaxis().SetTitleOffset(1.3)
       #pull_mode3.SetFillColor(39)



       ################################################## 
       #generate random error matrix
       ##################################################

       L=[x for x in range(1, DIM+1)]

       BINS=[x for x in itertools.product(L, L)]

       TO_PRINT=[]

       compare=dict()

       entry=0

       #print "*****************************************************"
       #print ENTRIES, matrix
       #print "-----------------------------------------------------"
       with open('prompt_'+argv[3]+'.json', 'w') as outfile:
           json.dump(matrix, outfile)
       #sys.exit()

       for x in range(1,ENTRIES+1):

           #print "entry=", x

#	   eigenvalues=dict()
#           eigenvectors=dict()

           eigenvalues=dict()
           eigenvectors=dict()

           generated_error_matrix=GET_MATRIX(error_matrix, BINS)
           sum_matrix=SUM_MATRIX(generated_error_matrix, matrix, BINS)

           EigenData(sum_matrix, 1, DIM, eigenvalues, eigenvectors) # GET MATRIX DATA
                                                                   #eigenvectors are in complex format R+iI

           pull_mode1.Fill(eigenvalues[1]/100)
           pull_mode2.Fill(eigenvalues[2]/10)
           pull_mode3.Fill(eigenvalues[3])
           pull_mode4.Fill(eigenvalues[4])

           
           COMPONENT_VECTORS=GET_COMPONENT_VECTORS(eigenvectors, DIM) # regroup eigenvectors in sets that contain 
                                                                      # the same alpha from all eigenvectors
                                                                      # indexation: 1,2,.....,N
           #print "EIGENVALUES:", eigenvalues, "EIGENVECTORS:", eigenvectors, "COMPONENT_VECTORS:", COMPONENT_VECTORS

           #signs = []

           for alpha in range(1, DIM+1):
           #for alpha in range(2, 3):

            
                   type=GET_TYPE(COMPONENT_VECTORS[str(alpha)])# check if all components are real and not complex
                                                                   #not complex type=0
                   
                   if type==0:
                          sign=GET_SIGN(COMPONENT_VECTORS[str(alpha)], REF_VECTORS[str(alpha)])#signs of components change
                                                                                               #even with same value; so need to add a steady sign
                          #signs.append(sign)
                          
                          for ei in range(0, DIM):
                          #for ei in range(DIM-1, DIM):

                                input=sign*(COMPONENT_VECTORS[str(alpha)][ei].real)
                                bin=alpha
                                #ei_histo[ei].Fill(bin, input)
                                #if bin==2: ei_histo_1D[ei].Fill(input)

                                if ACCOUNT_FIT and bin == 2:
                                    ei_histo[ei].Fill(bin, input, fns[alpha-1].Eval(input))
                                else:
                                    ei_histo[ei].Fill(bin, input)

                                if bin==2:
                                    if ACCOUNT_FIT:
                                        ei_histo_1D[ei].Fill(input, fns[alpha-1].Eval(input))
                                    else:
                                        ei_histo_1D[ei].Fill(input)

           #print "SIGNS", signs


        ################################################
        #GET VALUE AND ERROR OF EIGENVECTORS
        ################################################

       f_error=open(where_to_put+"/eigenvector_errors_"+str(DIM)+"x"+str(DIM)+".json", "w")
       f_simulated_eigenvectors =open(where_to_put+"/simulated_eigenvectors_"+str(DIM)+"x"+str(DIM)+".json", "w")

       simulated_eigenvectors_errors=dict()
       simulated_eigenvectors=dict()

       for which_vector in range(0,DIM):

           name="ei_Profile"+str(which_vector)
           ei_Profile=ei_histo[which_vector].ProfileX(name, 1, 30000, "S");

           temp_vector1=[]
           temp_vector2=[]
       
           for bin in range(1,DIM+1):

                  temp_vector1.append(ei_Profile.GetBinError(bin))
                  temp_vector2.append(ei_Profile.GetBinContent(bin))

           simulated_eigenvectors_errors[str(which_vector+1)]=temp_vector1
           simulated_eigenvectors[str(which_vector+1)]=temp_vector2


       json.dump(simulated_eigenvectors_errors, f_error, indent=2)
       #print "CIRKOVIC:", simulated_eigenvectors
       json.dump(simulated_eigenvectors, f_simulated_eigenvectors, indent=2)

        ################################################

       #################################################
       # GET LAMBDA VALUES
       #################################################

       f_simulated_eigenvalues =open(where_to_put+"/simulated_eigenvalues_"+str(DIM)+"x"+str(DIM)+".json", "w")
       f_lambda_error=open(where_to_put+"/eigenvalue_errors_"+str(DIM)+"x"+str(DIM)+".json", "w")

       simulated_eigenvalues=dict()
       simulated_eigenvalues_errors=dict()

       simulated_eigenvalues["1"]=100*pull_mode1.GetMean()
       if OLD:
           simulated_eigenvalues["2"]=10*pull_mode2.GetMean()
       else:
           #simulated_eigenvalues["2"]=1e-10
           #print "JSON MEAN:", pars["2.76TeV_00_02_n2_gfs_4_mode_2"][0][0][0]
           if GENMEAN:
               simulated_eigenvalues["2"]=pars["2.76TeV_"+cent+"_"+nx+"_gfs_"+str(2)+"_mode_2"][0][3][1]
           else:
               simulated_eigenvalues["2"]=pars["2.76TeV_"+cent+"_"+nx+"_gfs_"+str(2)+"_mode_2"][0][0][1]
       simulated_eigenvalues["3"]=pull_mode3.GetMean()
       simulated_eigenvalues["4"]=pull_mode4.GetMean()


       simulated_eigenvalues_errors["1"]=100*pull_mode1.GetRMS()
       if OLD:
          simulated_eigenvalues_errors["2"]=10*pull_mode2.GetRMS()
       else:
          #simulated_eigenvalues_errors["2"]=1e-100
          #print "JSON ERROR:", pars["2.76TeV_00_02_n2_gfs_4_mode_2"][0][0][1]
          if GENMEAN:
              simulated_eigenvalues_errors["2"]=pars["2.76TeV_"+cent+"_"+nx+"_gfs_"+str(2)+"_mode_2"][0][3][2]
          else:
              simulated_eigenvalues_errors["2"]=pars["2.76TeV_"+cent+"_"+nx+"_gfs_"+str(2)+"_mode_2"][0][0][2]
       simulated_eigenvalues_errors["3"]=pull_mode3.GetRMS()
       simulated_eigenvalues_errors["4"]=pull_mode4.GetRMS()

       #simulated_eigenvalues_errors["1"]=100*pull_mode1.GetMeanError()
       #simulated_eigenvalues_errors["2"]=10*pull_mode2.GetMeanError()
       #simulated_eigenvalues_errors["3"]=pull_mode3.GetMeanError()
       #simulated_eigenvalues_errors["4"]=pull_mode4.GetMeanError()

       json.dump(simulated_eigenvalues_errors, f_lambda_error, indent=2)
       json.dump( simulated_eigenvalues, f_simulated_eigenvalues, indent=2)

       print "RMS_L1=", pull_mode1.GetRMS()
       print "RMS_L2=", pull_mode2.GetRMS()

       #print "MEAN_L1=", pull_mode1.GetMeanError()
       #print "MEAN_L2=", pull_mode2.GetMeanError()


       root_file.Write()

main()
