import numpy as np
from scipy import linalg
import json
from sys import argv, exit
import cmath
import math
import functools
import operator
import itertools
from numpy import linalg as LA


def EigenData(Matrix, Xmin, Xmax, eigenvalues_dict, eigenvectors_dict):
   
   E = Matrix

   dim=int(math.sqrt(len(E)))
   DATA=[]
   
   ########################################
   # MAKE MATRIX
   ########################################
  
   for row in range(1,  dim+1):

         temp=[]
  
         for col in range(1, dim+1):

                  temp.append(E['V_'+str(row)+"_"+str(col)])

         DATA.append(temp) 

   A = np.array(DATA) #MATRIX

   ######################################## 
   # eigenvalues, eigenvectors
   ########################################

   eigenvalues, eigenvectors = linalg.eig(A)

   sorted_eigenvalues=list(reversed(sorted(eigenvalues)))

   count_eigen=0

   for x in sorted_eigenvalues:

           count_eigen=count_eigen+1

           eigenvalues_dict[count_eigen]=x.real


   count_eigen=0

   for x in eigenvectors:

           count_eigen=count_eigen+1

           eigenvectors_dict[count_eigen]=x.tolist()
   
   ####################################### PRINT
