import sys

#N=7
N=14

Nc = (N*(N-1))/2+N
print Nc

arr = []

for i in xrange(0, Nc):
    arr.append(i)

arr1 = arr[:-N]
arr2 = arr[-N:]

A = []
an = 0
for i in xrange(0, N):
    A.append(arr2[i])
    for j in xrange(i, N-1):
        A.append(arr1[an])
        an += 1

print arr1, arr2, A

sys.exit()

arr = []
n = 0
for i in xrange(0, N):
    arr.append([])
    for j in xrange(i, N):
        arr[-1].append(n)
        n += 1
A = []
for a in arr:
    for i in a[1:]:
        A.append(i)
for a in arr:
    A.append(a[0])

print A

sys.exit()

for i in xrange(0, N):
    for j in xrange(i, N):
        print (i, j)
