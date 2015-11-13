import glob
import subprocess32 as subprocess
import random
import codecs
from main import Thesis

random.seed(1)


train = sorted(glob.glob("Universal Dependencies/ud-treebanks-v1.1/*/*_vsrest-ud-train.conllu"))
dev = sorted(["-ud-dev".join(x.split("_vsrest-ud-train")) for x in train])
test =  sorted("-ud-test".join(x.split("_vsrest-ud-train")) for x in train)

for i in xrange(1):
	print train[i]
	print test[i]
	T = Thesis(train[i],test[i],FEAT=True)
	del T

"""
en_train = "Universal Dependencies/ud-treebanks-v1.1/UD_English/en_vsrest-ud-train.conllu"
en_test = "Universal Dependencies/ud-treebanks-v1.1/UD_English/en-ud-test.conllu"

bg_train = "Universal Dependencies/ud-treebanks-v1.1/UD_Bulgarian/bg_vsrest-ud-train.conllu"
bg_test = "Universal Dependencies/ud-treebanks-v1.1/UD_Bulgarian/bg-ud-test.conllu"
#en_output = "Data/en-ud-train.vw"

T1 = Thesis(en_train, en_test)
del T1

T2 = Thesis(bg_train,bg_test)
del T2

T3 = Thesis()
"""