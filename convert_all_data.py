import glob
import subprocess


train = glob.glob("Universal Dependencies/ud-treebanks-v1.1/*/*-ud-train.conllu")
dev = glob.glob("Universal Dependencies/ud-treebanks-v1.1/*/*-ud-dev.conllu")
test = glob.glob("Universal Dependencies/ud-treebanks-v1.1/*/*-ud-test.conllu")


illeagle = ["eu-ud-train.conllu","fr-ud-train.conllu","de-ud-train.conllu","id-ud-train.conllu","ga-ud-train.conllu","es-ud-train.conllu"]
print "Data_vw/UD/"+train[1].split("/")[-1][:-6]+"vw"
print "Data_vw/UD/"+dev[1].split("/")[-1][:-6]+"vw"
print "Data_vw/UD/"+test[1].split("/")[-1][:-6]+"vw"
print len(train)

for i in xrange(len(train)):
	if train[i].split("/")[-1] in illeagle:
		continue
	subprocess.Popen(["python","conll_to_vw/conll_to_vw.py",train[i],"Data_vw/UD/"+train[i].split("/")[-1][:-6]+"vw","--feature-set","dependency","--coarse"])
	subprocess.Popen(["python","conll_to_vw/conll_to_vw.py",dev[i],"Data_vw/UD/"+dev[i].split("/")[-1][:-6]+"vw","--feature-set","dependency","--coarse"])
	subprocess.Popen(["python","conll_to_vw/conll_to_vw.py",test[i],"Data_vw/UD/"+test[i].split("/")[-1][:-6]+"vw","--feature-set","dependency","--coarse"])
