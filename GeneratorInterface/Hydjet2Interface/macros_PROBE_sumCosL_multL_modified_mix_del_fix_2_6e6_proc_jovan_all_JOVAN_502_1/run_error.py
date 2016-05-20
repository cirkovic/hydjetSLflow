import json
import numpy as np
from numpy import array
from numpy import dot
from operator import add
import math
import os
from sys import argv, exit


def PROPAGATION(dL, de, L, e, M):

        print dL, de, L, e, M, "  "
        #M=1

        temp=[
             (1.0/(M*M))*(1.0/4) * (math.pow(e,2)/L) * math.pow(dL, 2) + 
             L * math.pow(de, 2)*(1.0/(M*M))
             ]

        if temp[0] >= 0:
            temp=math.sqrt(temp[0])
        else:
            temp=0

        return temp



def main():

          try:

               working_folder=str(argv[1])  #folder of eigenvalues and vectors
               degree_folder=str(argv[2])  #folder of eigenvalues and vectors

          except:

               print "didn't import eigen data files!"
               exit()

          DIM=11 

          #####################################################
          # READ FILES
          #####################################################

          mul_folder=working_folder
          working_folder=working_folder+"/"+degree_folder

      
          f1=open(working_folder+"/simulated_eigenvalues_"+str(DIM)+"x"+str(DIM)+".json", "r")  # 1-10 format
          f2=open(working_folder+ "/simulated_eigenvectors_"+str(DIM)+"x"+str(DIM)+".json", "r")  # 1-10 format

          f3=open(working_folder+"/eigenvector_errors_"+str(DIM)+"x"+str(DIM)+".json", "r")  # 1-10 format
          f4=open(working_folder+"/eigenvalue_errors_"+str(DIM)+"x"+str(DIM)+".json", "r")  # 1-10 format


          f5=open( mul_folder + "/Multiplicity.json", "r")  # 1-10 format



          #######################################################
          # calculate 
          #######################################################

          eigenvalues=json.load(f1)
          eigenvectors=json.load(f2)

          eigenvector_errors=json.load(f3)
          eigenvalue_errors=json.load(f4)

          M=json.load(f5)


          mode1_errors=dict()
          mode2_errors=dict()
          #mode3_errors=dict()
        
        
          L1=eigenvalues["1"]
          L2=eigenvalues["2"]
          L3=eigenvalues["3"]

          dL1=eigenvalue_errors["1"]
          dL2=eigenvalue_errors["2"]
          dL3=eigenvalue_errors["3"]


          for ei in range(1, DIM+1):

                temp_mode1=PROPAGATION(dL1, eigenvector_errors[str(ei)][0], L1, eigenvectors[str(ei)][0], M["P_"+str(ei)])
                temp_mode2=PROPAGATION(dL2, eigenvector_errors[str(ei)][1], L2, eigenvectors[str(ei)][1], M["P_"+str(ei)])
                #temp_mode3=PROPAGATION(dL3, eigenvector_errors[str(ei)][2], L3, eigenvectors[str(ei)][2], M["P_"+str(ei)])

                temp_mode1=round(temp_mode1, 6)
                temp_mode2=round(temp_mode2, 6)
                #temp_mode3=round(temp_mode3, 6)

          
                mode1_errors["P"+str(ei)]=temp_mode1
                mode2_errors["P"+str(ei)]=temp_mode2
                #mode3_errors["P"+str(ei)]=temp_mode3


          
          #########################################################
          # print
          ######################################################### 

          if not os.path.exists(working_folder+"/errors"):
              os.makedirs(working_folder+"/errors")



          f_mode1=open( working_folder+"/errors"+"/mode1_error.dat", "w")
          f_mode1_root=open( working_folder+"/errors"+"/root_format_mode1_error.dat", "w")

          f_mode2=open( working_folder+"/errors"+"/mode2_error.dat", "w")
          f_mode2_root=open( working_folder+"/errors"+"/root_format_mode2_error.dat", "w")

          #f_mode3= open( working_folder+"/errors"+"/mode3_error.dat", "w")
          #f_mode3_root=open( working_folder+"/errors"+"/root_format_mode3_error.dat", "w")

          f_mode1_root.write("{")
          f_mode2_root.write("{")
          #f_mode3_root.write("{")

          for ei in range(1, DIM+1):

                 f_mode1_root.write(str(mode1_errors["P"+str(ei)])), f_mode1_root.write(",")
                 f_mode2_root.write(str(mode2_errors["P"+str(ei)])), f_mode2_root.write(",")
                 #f_mode3_root.write(str(mode3_errors["P"+str(ei)])), f_mode3_root.write(",")

          f_mode1_root.write("};")
          f_mode2_root.write("};")
          #f_mode3_root.write("};")

          for ei in range(1, DIM+1):

                 f_mode1.write(str(mode1_errors["P"+str(ei)])), f_mode1.write("\n")
                 f_mode2.write(str(mode2_errors["P"+str(ei)])), f_mode2.write("\n")
                 #f_mode3.write(str(mode3_errors["P"+str(ei)])), f_mode3.write("\n")

main()
