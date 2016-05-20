import json

switches = [2]

#deltaEtaCuts = [1.0, 1.5, 2.0, 2.5, 3.0]
deltaEtaCuts = [2.0]

#centralities = ['00_02', '00_05', '00_10', '10_20', '20_30', '30_40', '40_50', '50_60']
centralities = ['00_05', '05_10', '10_15', '15_20', '20_25', '25_30', '30_35', '35_40', '40_50', '50_60', '60_70', '70_80']
#centralities = ['50_60']
#centralities = ['00_05']

for s in switches:
    for deta in deltaEtaCuts:
        de = str(deta)
        for c in centralities:
            for n in ["n2", "n3"]:
                d = {}
                dn = {
                    "mode1": "%s/%s/%s/%s/data_%s/modes/mode1.dat" % (s, de, c, c, n),
                    "mode1_error": "%s/%s/%s/%s/data_%s/errors/mode1_error.dat" % (s, de, c, c, n),
                    "mode2": "%s/%s/%s/%s/data_%s/modes/mode2.dat" % (s, de, c, c, n),
                    "mode2_error": "%s/%s/%s/%s/data_%s/errors/mode2_error.dat" % (s, de, c, c, n),
                }
                for key, value in dn.iteritems():
                    with open(value) as f:
                        d[key] = [abs(float(l)) if "mode1" in key else float(l) for l in f.readlines()]
                #print ("DATA/%s/%s_%s.json" % (n, s, c), d)
                #print ("DATA/%s/%s.json" % (n, c), d)
                with open("DATA/%s/%s/%s/%s.json" % (s, de, n, c), 'w') as fp:
                    json.dump(d, fp)

