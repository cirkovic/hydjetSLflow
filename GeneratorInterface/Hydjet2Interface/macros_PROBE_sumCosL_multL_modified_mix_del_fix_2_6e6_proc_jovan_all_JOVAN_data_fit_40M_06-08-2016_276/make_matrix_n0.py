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

PAIRS=dict()
TRACKS=dict()

PAIRS_error=dict()
TRACKS_error=dict()

BINS=[]
L1=[]

####################################
# GET MATRIX 
####################################


def GET_MATRIX(pairs, tracks):

   MATRIX=dict()

   for bin in BINS:

          if bin[0]==bin[1]:

                 #Vpipj= pairs["V_"+str(bin[0])+str(bin[1])] - tracks["T_"+str(bin[0])]*tracks["T_"+str(bin[1])] + tracks["T_"+str(bin[0])]
                 Vpipj= pairs["V_"+str(bin[0])+str(bin[1])] - tracks["T_"+str(bin[0])]*tracks["T_"+str(bin[1])] 
                     
                 MATRIX["V_"+str(bin[0])+str(bin[1])]=Vpipj

          if bin[0]!=bin[1]:

                   Vpipj= pairs["V_"+str(bin[0])+str(bin[1])] - tracks["T_"+str(bin[0])]*tracks["T_"+str(bin[1])]

                   MATRIX["V_"+str(bin[0])+str(bin[1])]=Vpipj
                   MATRIX["V_"+str(bin[1])+str(bin[0])]=Vpipj


   return MATRIX



#######################################


####################################
# GET MATRIX ERROR
####################################


def GET_MATRIX_ERROR(pairs, tracks, pairs_error, tracks_error):

   MATRIX=dict()

   for bin in BINS:

          if bin[0]==bin[1]:

               Vpipj= [
                        math.pow(pairs_error["V_"+str(bin[0])+str(bin[1])],2)

                      + math.pow(tracks["T_"+str(bin[0])],2)*math.pow(tracks_error["T_"+str(bin[1])],2)

                      + math.pow(tracks["T_"+str(bin[0])],2)*math.pow(tracks_error["T_"+str(bin[1])],2)

                      ]

               MATRIX["dV_"+str(bin[0])+str(bin[1])]=math.sqrt(Vpipj[0])

          if bin[0]!=bin[1]:

               Vpipj= [
                        math.pow(pairs_error["V_"+str(bin[0])+str(bin[1])],2)

                      + math.pow(tracks["T_"+str(bin[0])],2)*math.pow(tracks_error["T_"+str(bin[1])],2)

                      + math.pow(tracks["T_"+str(bin[0])],2)*math.pow(tracks_error["T_"+str(bin[1])],2)

                      ]

               MATRIX["dV_"+str(bin[0])+str(bin[1])]=math.sqrt(Vpipj[0])
               MATRIX["dV_"+str(bin[1])+str(bin[0])]=math.sqrt(Vpipj[0])


   return MATRIX


#######################################


#######################################
# GET PAIRS ERROR
#######################################

def GET_PAIRS_ERROR(path, f, Q):

      f.cd(path)

      for bin in BINS:


          histo_q1=(gDirectory.Get("Pairs_"+"P"+str(bin[0])+"P"+str(bin[1])))
          temp=histo_q1.GetMeanError()

          Q["V_"+str(bin[0])+str(bin[1])]=temp*1000


#######################################

#######################################
# GET TRACKS ERROR
#######################################

def GET_TRACKS_ERROR(path, f, Q):

      f.cd(path)

      for bin in L1:

        histo_q1=gDirectory.Get("P"+str(bin)+"_multiplicity")
        temp=histo_q1.GetMeanError()

        Q["T_"+str(bin)]=temp


#######################################



#######################################
# GET PAIRS
#######################################

def GET_PAIRS(path, f, Q):

      f.cd(path)

      for bin in BINS:

        histo_q1=(gDirectory.Get("Pairs_"+"P"+str(bin[0])+"P"+str(bin[1])))
        temp=histo_q1.GetMean()

        Q["V_"+str(bin[0])+str(bin[1])]=temp*1000


#######################################

#######################################
# GET TRACKS
#######################################

def GET_TRACKS(path, f, Q):

      f.cd(path)


      for bin in L1:

        histo_q1=gDirectory.Get("P"+str(bin)+"_multiplicity")
        temp=histo_q1.GetMean()

        Q["T_"+str(bin)]=temp


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
   
   ###############################################

   MIN=1
   MAX=int(dim)
   
   RANGE=str(dim)+"x"+str(dim)

   #global L1# WITHOUT this L1 is not seen in functions; but BINS work!

   L1_temp=[x for x in range(MIN, MAX+1)] #this or use of global
   for x in L1_temp: L1.append(x)

   for x in L1:

       for y in L1:

          if x>=y:

              BINS.append((y,x))

   ######################################### 
   # GET MULTIPLICITY
   #########################################

   f1.cd("PCA/Q_VALUES/"+centrality+"/Multiplicity")
   MULTIPLICITY=dict()

   for bin in range(1,int(dim)+1):

         histo=(gDirectory.Get("P"+str(bin)+"_multiplicity"))
         temp=histo.GetMean()
         MULTIPLICITY["P_"+ str(bin)]=temp



   ########################################

   #########################################
   # GET PAIRS and TRACKS
   #########################################  


   GET_PAIRS("PCA/Q_VALUES/"+centrality+"/Signal/n0/PAIRS_TOTAL", f1, PAIRS)
   GET_TRACKS("PCA/Q_VALUES/"+centrality+"/Multiplicity", f1, TRACKS)

   GET_PAIRS_ERROR("PCA/Q_VALUES/"+centrality+"/Signal/n0/PAIRS_TOTAL", f1, PAIRS_error)
   GET_TRACKS_ERROR("PCA/Q_VALUES/"+centrality+"/Multiplicity", f1, TRACKS_error)


   #########################################

   #########################################
   # GET MATRIX and PRINT
   #########################################

   os.chdir(FOLDER)

   SUB_folder_n0=centrality+"/data_n0"

   if not os.path.exists(SUB_folder_n0):
       os.makedirs(SUB_folder_n0)


   File=open("./" + SUB_folder_n0 +"/Matrix_n0_"+centrality+ "_"+RANGE + ".json", "w")
   File1=open("./"+ SUB_folder_n0 +"/Error_n0_"+centrality+ "_"+RANGE + ".json", "w")
   File2=open("./"+ SUB_folder_n0 +"/Tracks_"+centrality+".json", "w")


   MATRIX_n0=dict()
   MATRIX_n0_error=dict()


   MATRIX_n0=GET_MATRIX(PAIRS, TRACKS)
   MATRIX_n0_error=GET_MATRIX_ERROR(PAIRS, TRACKS, PAIRS_error, TRACKS_error)


   json.dump(MATRIX_n0, File, sort_keys=True, indent=2)   
   json.dump(MATRIX_n0_error, File1, sort_keys=True, indent=2)   
   json.dump(TRACKS, File2, sort_keys=True, indent=2)   


   ###########################################
   #Matrix n0
   ############################################


   ############################################


main()

