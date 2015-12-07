import glob
import subprocess32 as subprocess
import random
import codecs
from main import Thesis

random.seed(1)
#dev experiment
train = ["Universal Dependencies/ud-treebanks-v1.1/UD_Danish/da_vsrest-ud-train.conllu"]
dev = ["Universal Dependencies/ud-treebanks-v1.1/UD_Danish/da-ud-dev.conllu"]

"""
#Test experiment
train = sorted(glob.glob("Universal Dependencies/ud-treebanks-v1.1/*/*_vsrest-ud-train.conllu"))
dev = sorted(["-ud-dev".join(x.split("_vsrest-ud-train")) for x in train])
test =  sorted("-ud-test".join(x.split("_vsrest-ud-train")) for x in train)
"""

for i in xrange(1):
	print train[i]
	print dev[i]
	T = Thesis(train[i],dev[i],FEAT=False,SIZE=100,LOADMODEL=False,WINDOW=2,RETRO=True)
	del T