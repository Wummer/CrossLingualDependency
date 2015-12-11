import glob
import subprocess32 as subprocess
import random
import codecs
from main import Thesis

random.seed(1)
#dev experiment
"""
train = ["Universal Dependencies/ud-treebanks-v1.1/UD_Danish/da_vsrest-ud-train.conllu"]
test = ["Universal Dependencies/ud-treebanks-v1.1/UD_Danish/da-ud-dev.conllu"]

"""
#Test experiment
train = sorted(glob.glob("Universal Dependencies/ud-treebanks-v1.1/*/*_vsrest-ud-train.conllu"))
dev = sorted(["-ud-dev".join(x.split("_vsrest-ud-train")) for x in train])
test =  sorted("-ud-test".join(x.split("_vsrest-ud-train")) for x in train)

SIZE = 10
RETRO = True
LOAD = True

for i in xrange(len(train)):
	print train[i]
	print dev[i]
	T = Thesis(train[i],dev[i],FEAT=False,SIZE=SIZE,LOADMODEL=LOAD,WINDOW=2,RETRO=RETRO)
	del T

	path = "Data_vw/UD/"
	t = "-mvectors"+str(SIZE)+".vw"
	train_vw = path + train[i].split("/")[-1].replace(".conllu", t)
	test_vw = path + test[i].split("/")[-1].replace(".conllu", t)
	dev_vw = path + train[i].split("/")[-1].replace(".conllu", t)

	subprocess.call(["hanstholm/build/hanstholm","--d",train_vw,"--e",test_vw,
					"--template","thesis.txt", "--pred", "Results/UD/"+test_vw[11:-21]+"mvec"+str(SIZE)+"10retro.tsv"])

	subprocess.call(["hanstholm/build/hanstholm","--d",train_vw,"--e",test_vw,
					"--template","thesis2.txt", "--pred", "Results/UD/"+test_vw[11:-21]+"baseline.tsv"])