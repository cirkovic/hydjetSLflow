import math
import json
import os
import operator
from sys import argv, exit
import sys


def reconstruct(V1, V2):

     V12=zip(V1,V2)

     sum=0

     for x in V12:

           sum=sum + x[0]*x[1].conjugate()
      
     return sum

############################################

def get_modes(MODES, pt, Nmodes):

   modes=['m'+str(x) for x in range(1, Nmodes+1)] #m1, m2, ....mn

   V_pt1=[]

   for m in modes:

     temp1=complex(MODES["p"+str(pt)+m][0], MODES["p"+str(pt)+m][1])

     V_pt1.append(temp1)


   return V_pt1


def main():

    try:

         working_folder=str(argv[1])  
         DIM=str(argv[2])  
         sub_folder=str(argv[3])

    except:

         print "didn't import file"

         exit()

    EXT=DIM+"x"+DIM+".json"

    ##############################################
    # OPEN FILES
    ##############################################

    f1=open( working_folder+"/"+sub_folder+"/simulated_eigenvalues_"+EXT, "r")
    f2=open( working_folder+"/"+sub_folder+"/simulated_eigenvectors_"+EXT, "r")
    f3=open(working_folder+"/Multiplicity.json", "r")
  
    ##############################################
    # calculate
    ##############################################

    eigenvalues =json.load(f1)
    eigenvectors =json.load(f2)

    Multiplicity =json.load(f3)

    DIM=len(Multiplicity) 


    mode1=[]
    mode2=[]
    mode3=[]
    mode4=[]

    for ei in range(1, DIM+1):

           if eigenvalues["1"] >= 0:
               temp1=(math.sqrt(eigenvalues["1"])*eigenvectors[str(ei)][0])/Multiplicity["P_"+str(ei)]
           else:
               temp1=(math.sqrt(0)*eigenvectors[str(ei)][0])/Multiplicity["P_"+str(ei)]
           if eigenvalues["2"] >= 0:
               temp2=(math.sqrt(eigenvalues["2"])*eigenvectors[str(ei)][1])/Multiplicity["P_"+str(ei)]
           else:
               temp2=(math.sqrt(0)*eigenvectors[str(ei)][1])/Multiplicity["P_"+str(ei)]
           if eigenvalues["3"] >= 0:
               temp3=(math.sqrt(eigenvalues["3"])*eigenvectors[str(ei)][2])/Multiplicity["P_"+str(ei)]
           else:
               temp3=(math.sqrt(0)*eigenvectors[str(ei)][2])/Multiplicity["P_"+str(ei)]
           #temp4=(math.sqrt(eigenvalues["4"])*eigenvectors[str(ei)][3])/Multiplicity["P_"+str(ei)]

           #temp1=(math.sqrt(eigenvalues["1"])*eigenvectors[str(ei)][0])#/Multiplicity["P_"+str(ei)]
           #temp2=(math.sqrt(eigenvalues["2"])*eigenvectors[str(ei)][1])#/Multiplicity["P_"+str(ei)]
           #temp3=(math.sqrt(eigenvalues["3"])*eigenvectors[str(ei)][3])#/Multiplicity["P_"+str(ei)]

           temp1=round(temp1, 5)
           temp2=round(temp2, 5)
           temp3=round(temp3, 5)

           mode1.append(temp1)
           mode2.append(temp2)
           mode3.append(temp3)
           #mode4.append(temp4)


    ###############################################
    # print
    ###############################################

    if not os.path.exists(working_folder+"/"+sub_folder+"/modes"):

              os.makedirs(working_folder+"/"+sub_folder+"/modes")

    W=working_folder+"/"+sub_folder+"/modes/"

    f_mode1=open(W+"mode1.dat", "w")
    f_mode1_root=open( W+"root_format_mode1.dat", "w")

    f_mode2=open(W+"mode2.dat", "w")
    f_mode2_root=open( W+"root_format_mode2.dat", "w")

    f_mode3=open( W+"mode3.dat", "w")
    f_mode3_root=open( W+"root_format_mode3.dat", "w")

    f_mode4=open( W+"mode4.dat", "w")
    f_mode4_root=open( W+"root_format_mode4.dat", "w")

    f_mode1_root.write("{")
    f_mode2_root.write("{")
    f_mode3_root.write("{")
    f_mode4_root.write("{")

    for pt in range(0, DIM):

            f_mode1_root.write(str(mode1[pt])), f_mode1_root.write(",")
            f_mode2_root.write(str(mode2[pt])), f_mode2_root.write(",")
            f_mode3_root.write(str(mode3[pt])), f_mode3_root.write(",")
            #f_mode4_root.write(str(mode4[pt])), f_mode4_root.write(",")

    f_mode1_root.write("};")
    f_mode2_root.write("};")
    f_mode3_root.write("};")
    f_mode4_root.write("};")

    for pt in range(0, DIM):

            f_mode1.write(str(mode1[pt])), f_mode1.write("\n")
            f_mode2.write(str(mode2[pt])), f_mode2.write("\n")
            f_mode3.write(str(mode3[pt])), f_mode3.write("\n")
            #f_mode4.write(str(mode4[pt])), f_mode4.write("\n")


    
main()
 
