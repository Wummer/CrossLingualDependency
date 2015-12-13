import glob
import subprocess32 as subprocess
import random
import codecs
from main import Thesis

random.seed(1)
# dev experiment

train = "Universal Dependencies/ud-treebanks-v1.1/UD_Danish/da_vsrest-ud-train.conllu"
test = "Universal Dependencies/ud-treebanks-v1.1/UD_Danish/da-ud-dev.conllu"


SIZE = [10, 25, 50]
WINDOW = [1, 2, 3]
RETRO = True
LOAD = False

for size in SIZE:
    for window in WINDOW:
        T = Thesis(
            train, test, SIZE=size, LOADMODEL=LOAD, WINDOW=window, RETRO=RETRO)
        LOAD = True
        del T

        path = "Data_vw/UD/"
        t = "-mvectors" + str(size) + ".vw"
        train_vw = path + train.split("/")[-1].replace(".conllu", t)
        test_vw = path + test.split("/")[-1].replace(".conllu", t)
        dev_vw = path + train.split("/")[-1].replace(".conllu", t)
        results = "Results/UD/" + \
            test_vw[11:-21] + "-dev-mvec" + \
            str(size) + "-" + "win" + str(window) + "retro.tsv"
        print results

        subprocess.call(["hanstholm/build/hanstholm", "--d", train_vw, "--e", test_vw,
                         "--template", "thesis.txt", "--pred", results])

        subprocess.call(["hanstholm/build/hanstholm", "--d", train_vw, "--e", test_vw,
                         "--template", "thesis3.txt", "--pred", results[:-4]+"-nowords.tsv"])

    LOAD = False

subprocess.call(["hanstholm/build/hanstholm", "--d", train_vw, "--e", test_vw,
                 "--template", "thesis2.txt", "--pred", "Results/UD/" + test_vw[11:-21] + "baseline.tsv"])
subprocess.call(["hanstholm/build/hanstholm", "--d", train_vw, "--e", test_vw,
                 "--template", "thesis4.txt", "--pred", "Results/UD/" + test_vw[11:-21] + "baseline-nowords.tsv"])
