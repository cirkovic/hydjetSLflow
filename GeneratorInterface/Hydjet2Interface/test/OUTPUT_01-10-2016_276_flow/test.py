terms = []
for i in xrange(1, 11):
    terms.append("2*["+str(i)+"]*cos("+str(i)+"*x)")
terms = "+".join(terms)
print terms
