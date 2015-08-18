tot = 30186
both = 601
a = 61
b = 37
none = tot-both-a-b
pra = 1.0*(both+none)/tot
print "Pr(a)",pra
ayes = 1.0*(both+a)/tot
byes = 1.0*(both+b)/tot
ano = 1-ayes
bno = 1-byes
#print ayes,byes
#print ano,bno
bothyes = ayes*byes
bothno = ano*bno
pre = bothyes+bothno
print "Pr(e)",pre
kappa = (pra-pre)/(1-pre)
print "Kappa",kappa
