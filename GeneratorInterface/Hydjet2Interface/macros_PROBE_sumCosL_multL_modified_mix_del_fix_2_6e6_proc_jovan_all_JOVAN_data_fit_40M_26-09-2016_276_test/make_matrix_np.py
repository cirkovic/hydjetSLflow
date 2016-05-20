import ROOT
from ROOT import gDirectory
import json
import os
import math
import itertools
from sys import argv

####################################
# global variables
####################################

EVENT_NUMBER=dict()
EVENT_NUMBER_BACK=dict()

COS_n0=dict()
COS_n2=dict()
COS_n3=dict()

COS_n2_BACK=dict()  
COS_n3_BACK=dict()  

COS_n2_error=dict()
COS_n3_error=dict()

COS_n2_BACK_error=dict()  
COS_n3_BACK_error=dict()  


FRACTION=dict()
FRACTION_BACK=dict()

BINS=[]# to be read by all methods

####################################


####################################
# GET MATRIX 
####################################


def GET_MATRIX(SIGNAL, BACKGROUND = None):

   MATRIX=dict()

   for bin in BINS:

          fracS=FRACTION["V_"+str(bin[0])+str(bin[1])]
          #fracS = 1
          #fracB=FRACTION_BACK["V_"+str(bin[0])+str(bin[1])]


          #Vpipj= 5*(fracS)*(SIGNAL["V_"+str(bin[0])+str(bin[1])]) - 50*(fracB)*(BACKGROUND["V_"+str(bin[0])+str(bin[1])])
          Vpipj= 5*(fracS)*(SIGNAL["V_"+str(bin[0])+str(bin[1])])# - 50*(fracB)*(BACKGROUND["V_"+str(bin[0])+str(bin[1])])
          Vpipj= 5*(fracS)*(SIGNAL["V_"+str(bin[0])+str(bin[1])])# - 50*(fracB)*(BACKGROUND["V_"+str(bin[0])+str(bin[1])])
                     
          MATRIX["V_"+str(bin[0])+str(bin[1])]=Vpipj

          if bin[0]!=bin[1]:

                   MATRIX["V_"+str(bin[1])+str(bin[0])]=Vpipj


   return MATRIX


#######################################
# GET ERROR MATRIX
#######################################

def GET_MATRIX_ERROR(sig_error, back_error = None):

        matrix=dict()

        for bin in BINS: 


               error_sig=math.pow(FRACTION["V_"+str(bin[0])+str(bin[1])], 2)*math.pow(sig_error["V_"+str(bin[0])+str(bin[1])],2)
               #error_back=math.pow(FRACTION_BACK["V_"+str(bin[0])+str(bin[1])], 2)*math.pow(back_error["V_"+str(bin[0])+str(bin[1])],2) 

             
               #matrix["dV_"+str(bin[0])+str(bin[1])]=5*math.sqrt(error_sig + 100*error_back)
               matrix["dV_"+str(bin[0])+str(bin[1])]=5*math.sqrt(error_sig)

               #if bin[0]!=bin[1]: matrix["dV_"+str(bin[1])+str(bin[0])]=5*math.sqrt(error_sig + 100*error_back)
               if bin[0]!=bin[1]: matrix["dV_"+str(bin[1])+str(bin[0])]=5*math.sqrt(error_sig)


        return matrix

#######################################


#######################################
# GET COS VALUE
#######################################

def GET_COS_VALUE(path, f, Q):

      f.cd(path)

      for bin in BINS:

        histo_q1=(gDirectory.Get("cosDelta_"+"P"+str(bin[0])+"P"+str(bin[1])))
        temp=histo_q1.GetMean()

        Q["V_"+str(bin[0])+str(bin[1])]=temp


#######################################

#######################################
# GET COS VALUE ERROR
#######################################

def GET_COS_VALUE_ERROR(path, f, Q):

      f.cd(path)

      for bin in BINS:

        histo_q1=(gDirectory.Get("cosDelta_"+"P"+str(bin[0])+"P"+str(bin[1])))
        temp=histo_q1.GetMeanError()

        Q["V_"+str(bin[0])+str(bin[1])]=temp


#######################################




def main():

   ##############################################
   # GET FILE
   ##############################################
  
   
   try:

       centrality=str(argv[1]) # which centrality folder; needs to be without the \
       FOLDER=str(argv[2]) # which centrality folder; needs to be without the \
       dim=str(argv[3]) # which centrality folder; needs to be without the \

   except:

       print "didn't import working folder"


   f1 = ROOT.TFile("./" + FOLDER + "/out_"+centrality+".root")

   RANGE=str(dim)+"x"+str(dim)
   
   MIN=1
   MAX=int(dim)


   ###############################################
   
   ########################################
   # MATRIX RANGE
   ########################################

   L1=[x for x in range(MIN, MAX+1)]

   for x in L1:

          for y in L1:

                  if x>=y:

                     BINS.append((y,x))    


   ######################################### 
   # GET EVENT NUMBER; COUNT
   #########################################

   f1.cd("PCA/Q_VALUES/"+centrality)

   histo=(gDirectory.Get("Event_count"))
   histo_back=(gDirectory.Get("Event_count_back"))

   for bin in BINS:

         temp=histo.GetBinContent(bin[0], bin[1])
         EVENT_NUMBER["P"+str(bin[0])+str(bin[1])]=temp

   for bin in BINS:

         temp=histo_back.GetBinContent(bin[0], bin[1])
         EVENT_NUMBER_BACK["P"+str(bin[0])+str(bin[1])]=temp

   ########################################

   ######################################### 
   # GET MULTIPLICITY
   #########################################

   f1.cd("PCA/Q_VALUES/"+centrality+"/Multiplicity")
   MULTIPLICITY=dict()

   for bin in range(1,MAX+1):

         histo=(gDirectory.Get("P"+str(bin)+"_multiplicity"))
         temp=histo.GetMean()
         MULTIPLICITY["P_"+ str(bin)]=temp



   ########################################

   #######################################
   # FRACTION
   #######################################

   f1.cd("PCA/Q_VALUES/"+centrality)
 
   histo_fraction=(gDirectory.Get("pair_fraction"))
   histo_fraction_back=(gDirectory.Get("pair_fraction_back"))

   for bin in BINS:


         temp=histo_fraction.GetBinContent(bin[0], bin[1])
         temp_average=temp/EVENT_NUMBER["P"+str(bin[0])+str(bin[1])]

         FRACTION["V_"+str(bin[0])+str(bin[1])]=1.0/temp_average

   for bin in BINS:


         temp=histo_fraction_back.GetBinContent(bin[0], bin[1])
         temp_average=temp/EVENT_NUMBER_BACK["P"+str(bin[0])+str(bin[1])]

         FRACTION_BACK["V_"+str(bin[0])+str(bin[1])]=1.0/temp_average


   #########################################
   # GET SIGNAL n2, n3
   #########################################  


   GET_COS_VALUE("PCA/Q_VALUES/"+centrality+"/Signal/n2/COS_NOT_NORMED", f1, COS_n2)
   GET_COS_VALUE("PCA/Q_VALUES/"+centrality+"/Signal/n3/COS_NOT_NORMED", f1, COS_n3)

   GET_COS_VALUE_ERROR("PCA/Q_VALUES/"+centrality+"/Signal/n2/COS_NOT_NORMED", f1, COS_n2_error)
   GET_COS_VALUE_ERROR("PCA/Q_VALUES/"+centrality+"/Signal/n3/COS_NOT_NORMED", f1, COS_n3_error)


   #########################################
   #BACKGROUND n2, n3
   ########################################


   #GET_COS_VALUE("PCA/Q_VALUES/"+centrality+"/Background/n2/COS_NOT_NORMED", f1, COS_n2_BACK)
   #GET_COS_VALUE("PCA/Q_VALUES/"+centrality+"/Background/n3/COS_NOT_NORMED", f1, COS_n3_BACK)

   #GET_COS_VALUE_ERROR("PCA/Q_VALUES/"+centrality+"/Background/n2/COS_NOT_NORMED", f1, COS_n2_BACK_error)
   #GET_COS_VALUE_ERROR("PCA/Q_VALUES/"+centrality+"/Background/n3/COS_NOT_NORMED", f1, COS_n3_BACK_error)


   #########################################

   #########################################
   # GET MATRIX and PRINT
   #########################################

   os.chdir(FOLDER)

   MATRIX_n0=dict()
   MATRIX_n2=dict()
   MATRIX_n3=dict()

   MATRIX_n0_error=dict()
   MATRIX_n2_error=dict()
   MATRIX_n3_error=dict()

   SUB_folder_n2=centrality+"/data_n2_np"
   SUB_folder_n3=centrality+"/data_n3_np"
   
   if not os.path.exists(SUB_folder_n2):
    os.makedirs(SUB_folder_n2)

   if not os.path.exists(SUB_folder_n3):
    os.makedirs(SUB_folder_n3)


   File2=open("./"+SUB_folder_n2+"/Matrix_n2_"+centrality+ "_"+RANGE + ".json", "w")
   File3=open("./"+SUB_folder_n3+"/Matrix_n3_"+centrality+ "_"+RANGE + ".json", "w")

   
   #File4=open("../Pairs.json", "w")
   File5=open(centrality+"/Multiplicity.json", "w")

   MATRIX_n2 =GET_MATRIX(COS_n2)#, COS_n2_BACK)
   MATRIX_n3 =GET_MATRIX(COS_n3)#, COS_n3_BACK)

   File2_error=open("./"+ centrality+"/data_n2_np/Error_n2_"+centrality+ "_"+RANGE+".json", "w")
   File3_error=open("./"+ centrality+"/data_n3_np/Error_n3_"+centrality+ "_"+RANGE +".json", "w")
   
   MATRIX_n2_error =GET_MATRIX_ERROR(COS_n2_error)#, COS_n2_BACK_error)
   MATRIX_n3_error =GET_MATRIX_ERROR(COS_n3_error)#, COS_n3_BACK_error)

   ###########################################
   #Matrix n0
   ############################################


   ############################################


   json.dump(MATRIX_n2, File2, sort_keys=True, indent=2)
   json.dump(MATRIX_n3, File3, sort_keys=True, indent=2)

   json.dump(MATRIX_n2_error, File2_error, sort_keys=True, indent=2)
   json.dump(MATRIX_n3_error, File3_error, sort_keys=True, indent=2)

   json.dump(MULTIPLICITY, File5, sort_keys=True, indent=2)

main()

