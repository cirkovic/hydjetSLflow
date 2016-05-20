import numpy as np
from scipy import linalg as la
import sys
import pprint
import random
from datetime import datetime
random.seed(datetime.now())

#import sys
#sys.path.append('./scipy/scipy/linalg')
#from _solvers import solve_sylvester
#sys.path.append('./control/control')
#from mateqn import lyap

WITHOUT_M1 = False


M1 = np.array([[1., -2., 3.], [-4., 5., -6.], [-7., 8., -9.]])
M1 = np.array([[-52., -22.], [110., 47.]])

if WITHOUT_M1:
    EIGENVALUES = np.array([2439.8236372731531, 1.261670830339821, 0.79151500664157881, 0.13645398951875279, 0.10154777179889014, 0.0032443939086390541, -0.58604280713164858])

    EIGENVECTORS = np.array([
    [-0.41558814939555144, 0.5848162937026418, 0.5039246965853996, -0.5561881532131379, -0.04719304945630682, -0.2125074665681551, 0.1724381127534817],
    [-0.5584524476587333, -0.2899514095804062, 0.3475179691013286, 0.6933533652784177, -0.04585359027676074, 0.2246030432046692, -0.4568370411854932],
    [-0.44861014515039166, 0.4537396399776695, -0.7208824790526347, -0.43998637570244375, 0.08363246984667191, 0.2245570635769877, -0.021326905049839376],
    [-0.5169343197023661, -0.36907049090977556, -0.18615272833432553, 0.107485384642584, -0.003686924333744523, -0.21603456322506717, 0.5865270291980652],
    [-0.20274402287504434, -0.3385816026170034, -0.016219493600663066, -0.06904671547145085, -0.0679021722188166, -0.3880295999121914, -0.4709765564537424],
    [-0.07226425854953976, -0.28476490470074417, 0.21169738179165726, -0.0023837787836936955, 0.5964082862228227, 0.5104121686230336, -0.05228316921185556],
    [-0.02485837268760104, -0.18999168922579474, 0.160897237457673, -0.0012645347883269672, -0.7926845097835393, 0.6294518965253324, -0.43879810357398713]
    ])
else:
    EIGENVALUES, EIGENVECTORS = la.eig(M1)

print '###############################################'

L = np.matrix(np.diag(EIGENVALUES))
V = np.array(EIGENVECTORS)
Vinv = la.inv(V)
V_temp = np.array(V)

M2 = np.dot(np.dot(V, L), Vinv)

eival, eivec = la.eig(M2)


print M1.real
print M2.real

print

print EIGENVALUES.real
print eival.real

print

print EIGENVECTORS.real
print eivec.real

'''

if not WITHOUT_M1:
    print np.multiply(np.fabs(np.divide(np.subtract(M2.real, M1.real), M1.real)), 100)

    print

print np.multiply(np.fabs(np.divide(np.subtract(eival.real, EIGENVALUES.real), EIGENVALUES.real)), 100)

print

print np.multiply(np.fabs(np.divide(np.subtract(eivec.real, V.real), V.real)), 100)
'''
print '###############################################'

L = np.array(np.diag(EIGENVALUES))
V = np.array(EIGENVECTORS)

SCALE = 1e-2

Vshape = V.shape
for yi in xrange(0, Vshape[0]):
    for xi in xrange(0, Vshape[1]):
        V[yi][xi] = V[yi][xi]-random.uniform(0, SCALE*V[yi][xi])

#Lshape = L.shape
#for yi in xrange(0, Lshape[0]):
#    for xi in xrange(0, Lshape[1]):
#        if xi == yi:
#            L[yi][xi] = L[yi][xi]-random.uniform(0, SCALE*L[yi][xi])

Vinv = la.inv(V)

signs = np.divide(V, np.fabs(V))
#print signs

M2 = np.dot(np.dot(V, L), Vinv)

eival, eivec = la.eig(M2)
eivec = np.multiply(signs, np.fabs(eivec.real))

#X = solve_sylvester(M2, np.negative(M1), np.zeros_like(M2))
#print X

#M2inv = la.inv(M2)
#M1inv = la.inv(M1)
#M3 = np.dot(np.dot(np.dot(M2inv, V), L), la.inv(np.dot(M1inv, V)))
#eival3 = np.dot(M1inv, V)
#eivec3 = np.multiply(signs, np.fabs(V.real))

print M1.real
print M2.real
#print M3.real

print

print EIGENVALUES.real
print eival.real
#print eival3.real

print

print EIGENVECTORS.real
print eivec.real
#print eivec3.real

'''

if not WITHOUT_M1:
    print np.multiply(np.fabs(np.divide(np.subtract(M2.real, M1.real), M1.real)), 100)

    print

print np.multiply(np.fabs(np.divide(np.subtract(eival.real, EIGENVALUES.real), EIGENVALUES.real)), 100)

print

print np.multiply(np.fabs(np.divide(np.subtract(eivec.real, V.real), V.real)), 100)
'''
print '###############################################'

#print np.multiply(np.fabs(np.divide(np.subtract(V.real, V_temp.real), V_temp.real)), 100)

#print '###############################################'
