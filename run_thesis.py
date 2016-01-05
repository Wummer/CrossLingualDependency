import glob
import subprocess
import random
import codecs
import sys
from main import Thesis

random.seed(1)
print 
DATASET = str(sys.argv[1])

try:
    if str(sys.argv[2]) == "RBG":
        RBG = True
    else: RBG=False
except IndexError:
    RBG = False

SIZE = 25
RETRO = True
LOAD = False
WINDOW = 1


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
    test = sorted("test".join(x.split("train")) for x in train)

elif DATASET == "SPMRL":
    train = sorted(glob.glob("SPMRL mapped/*/*_vsrest-spmrl-train5k.conllu"))
    test = sorted("test".join(x.split("train5k"))
                  for x in train)
else:
    print sys.argv[1]
    print "Expected UD or SPMRL as argument 1"
    raise SystemExit



if RBG == False:
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
                test_vw[11:-21] + "-mvec" + \
                str(SIZE) + "-" + "win" + str(WINDOW) + "retro.tsv"

        elif DATASET == "SPMRL":
            results = "Results/" + DATASET + "/" + \
                test_vw[14:-19] + "-mvec" + \
                str(SIZE) + "-" + "win" + str(WINDOW) + "retro.tsv"

        subprocess.call(["hanstholm/build/hanstholm", "--d", train_vw, "--e", test_vw,
                         "--template", "nivre.txt", "--pred", results[:-4] + "-nivre.tsv"])

        subprocess.call(["hanstholm/build/hanstholm", "--d", train_vw, "--e", test_vw,
                         "--template", "nivre3.txt", "--pred", results[:-4] + "-nivre3.tsv"])

        subprocess.call(["hanstholm/build/hanstholm", "--d", train_vw, "--e", test_vw,
                         "--template", "thesis5.txt", "--pred", results[:-4] + "-wals5.tsv"])

        subprocess.call(["hanstholm/build/hanstholm", "--d", train_vw, "--e", test_vw,
                         "--template", "thesis.txt", "--pred", results])

        subprocess.call(["hanstholm/build/hanstholm", "--d", train_vw, "--e", test_vw,
                         "--template", "thesis3.txt", "--pred", results[:-4] + "-nowords.tsv"])
        """
        subprocess.call(["hanstholm/build/hanstholm", "--d", train_vw, "--e", test_vw,
                         "--template", "thesis4.txt", "--pred", results.split("-")[0] + "-baseline-nowords.tsv"])

        subprocess.call(["hanstholm/build/hanstholm", "--d", train_vw, "--e", test_vw,
                         "--template", "thesis2.txt", "--pred", results.split("-")[0] + test_vw[14:-119] + "-baseline.tsv"])
        """

if RBG == True:
    for i in xrange(len(train)):

        print train[i]
        T = Thesis(train[i], test[i], DATA=DATASET, SIZE=SIZE,
                   LOADMODEL=LOAD, WINDOW=WINDOW, RETRO=RETRO, RBG=RBG,WORKERS=1)
        del T   