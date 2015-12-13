import glob
import subprocess
import random
import codecs
import sys
from main import Thesis

random.seed(1)
DATASET = str(sys.argv[1])

if DATASET == "UD":
    # dev experiment
    """
    train = [
        "Universal Dependencies/ud-treebanks-v1.1/UD_Danish/da_vsrest-ud-train.conllu"]
    test = ["Universal Dependencies/ud-treebanks-v1.1/UD_Danish/da-ud-dev.conllu"]

    """
    # Test experiment
    train = sorted(
        glob.glob("Universal Dependencies/ud-treebanks-v1.1/*/*_vsrest-ud-train.conllu"))
    test = sorted("-ud-test".join(x.split("_vsrest-ud-train")) for x in train)

elif DATASET == "SPMRL":
    train = sorted(glob.glob("SPMRL mapped/*/*_vsrest-spmrl-train5k.conllu"))
    test = sorted("-spmrl-test".join(x.split("_vsrest-spmrl-train")) for x in train)
else:
    print sys.argv[1]
    print "Expected UD or SPMRL as argument 1"
    raise SystemExit


SIZE = 50
RETRO = True
LOAD = False
WINDOW = 2

for i in xrange(len(train)):
    print train[i]
    T = Thesis(train[i], test[i], DATA=DATASET, SIZE=SIZE,
               LOADMODEL=LOAD, WINDOW=WINDOW, RETRO=RETRO)
    del T

    path = "Data_vw/" + DATASET + "/"
    t = "-mvectors" + str(SIZE) + ".vw"
    train_vw = path + train[i].split("/")[-1].replace(".conllu", t)
    test_vw = path + test[i].split("/")[-1].replace(".conllu", t)

    if DATASET == "UD":
    	results = "Results/" + DATASET + "/" + \
        	test_vw[11:-21] + "-dev-mvec" + \
        	str(SIZE) + "-" + "win" + str(WINDOW) + "retro.tsv"
    
    elif DATASET == "SPMRL":
    	results = "Results/" + DATASET + "/" + \
    	test_vw[14:-21] + "-dev-mvec" + \
        str(SIZE) + "-" + "win" + str(WINDOW) + "retro.tsv"

    subprocess.call(["hanstholm/build/hanstholm", "--d", train_vw, "--e", test_vw,
                     "--template", "thesis.txt", "--pred", results])

    subprocess.call(["hanstholm/build/hanstholm", "--d", train_vw, "--e", test_vw,
                     "--template", "thesis2.txt", "--pred", results[:-3] + "-nowords.tsv"])
