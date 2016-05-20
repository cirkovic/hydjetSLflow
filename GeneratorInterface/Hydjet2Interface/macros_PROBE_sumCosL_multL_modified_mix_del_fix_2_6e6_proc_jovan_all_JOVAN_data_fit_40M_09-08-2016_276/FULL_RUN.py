from subprocess import call
from sys import argv
import sys, os
import json

#print sys.argv

#sys.exit()


def main():


    ##################################################
    # SET input values
    ##################################################

    #f=open('Parameters.json', 'r')
    f=open('../../Parameters_'+sys.argv[1]+'.json', 'r')

    Parameters=json.load(f)

    cent=Parameters['centralities']
    FOLDER=Parameters['working folder']
    DIM=Parameters["dim of matrix"]
    iter=Parameters["number of iterations"]
    SPLIT=Parameters["SPLIT"]
    

    ###################################################
    # MAKE MATRIX
    ###################################################

    for x in cent:

          #print "CALCULATING MATRIX.........n0\n\n"
          #call(['python', 'make_matrix_n0.py', x, FOLDER, str(DIM)])

          print "CALCULATING MATRIX.........n23\n\n"
          if SPLIT==False: call(['python', '../../make_matrix.py', x, FOLDER, str(DIM)])
#          if SPLIT==True: 
#                 call(['python', '../../make_matrix_normed_split.py', x, FOLDER, str(DIM)])
#                 call(['python', '../../make_matrix_split.py', x, FOLDER, str(DIM)])

          print "finished process\n", 
          print '##############################\n\n'

    ###################################################
    # EIGENVALUES AND EIGENVECTORS
    ###################################################

    for x in cent:

          working_folder=FOLDER+"/"+x

          #print "MATRIX PERMUTATION.....n0\n\n "
          #call(['python', 'run_matrix_n0.py', working_folder+"/data_n0", str(iter)])

          print "MATRIX PERMUTATION.....n2\n\n "
          call(['python', '../../run_matrix.py', working_folder+"/data_n2", str(iter)])

          print "MATRIX PERMUTATION.....n3\n\n "
          call(['python', '../../run_matrix.py', working_folder+"/data_n3", str(iter)])

          print "finished process\n", 
          print '##############################\n\n'

    ####################################################
    # MODES
    ####################################################

    for x in cent:

        #print "MODES.....n0\n\n "
        #call(['python', 'calculate_modes.py', working_folder, str(DIM), "data_n0"])

        print "MODES.....n2\n\n "
        call(['python', '../../calculate_modes.py', working_folder, str(DIM), "data_n2"])

        print "MODES.....n3\n\n "
        call(['python', '../../calculate_modes.py', working_folder, str(DIM), "data_n3"])

        print "finished process\n", 
        print '##############################\n\n'

    ###################################################
    # run_mode_error.py
    ###################################################
    
    for x in cent:
                 
                  working_folder=FOLDER+"/"+x

                  #print "MODES.....n0\n\n "
                  #call(['python', 'run_error.py', working_folder, "data_n0"])

                  print "MODES.....n2\n\n "
                  call(['python', '../../run_error.py', working_folder, "data_n2"])

                  print "MODES.....n3\n\n "
                  call(['python', '../../run_error.py', working_folder, "data_n3"])

                  print "finished process", '\n\n\n\n'

    command="ddd"

    if command=="rn":

           for x in cent:

                  folder=FOLDER+ x + "/data_n2/modes"
                  folder_error=FOLDER+ x + "/data_n2/errors"

                  call(['python', 'rn.py', folder, folder_error])

                  folder=FOLDER+ x + "/data_n2/modes"

                  #call(['python', 'rn.py', folder])

                  print "finished process", '\n\n\n\n'

    if command=="RN":

           for x in cent:

                  folder_eff=FOLDER+ x + "/data_n2/"
                  folder=FOLDER+ x + "/data_n2/"
                   
                  call(['python', 'RN.py', folder, x, str(DIM)])

                  folder=FOLDER+ x + "/data_n3/"

                  #call(['python', 'RN.py', folder, x])

                  print "finished process", '\n\n\n\n'


main()
