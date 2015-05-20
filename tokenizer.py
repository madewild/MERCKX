import nltk, codecs

f = open("yperling.txt").readlines()
o = open("ype_output", "a")
for l in f:
  words = nltk.word_tokenize(l)
  for w in words:
    o.write(w)
    o.write(" ")
    o.write("\n")
