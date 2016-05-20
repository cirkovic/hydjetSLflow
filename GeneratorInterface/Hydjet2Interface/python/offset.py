import sys

#print "CIRKOVICARGV", sys.argv

INEVT=0
ISWTC=1
ICENT=2
IDETC=3
IENRG=4
IINDX=5

offset = 0

for i, a in enumerate(sys.argv):
    if '.py' in a:
        offset = i + 1
        break

argv = sys.argv[offset:len(sys.argv)]
print "CIRKOVICARG", argv

#sys.exit()
