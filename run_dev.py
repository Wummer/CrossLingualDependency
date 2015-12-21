import glob
import subprocess32 as subprocess
import random
import codecs
import sys
from main import Thesis

random.seed(1)
# dev experiment

train = "Universal Dependencies/ud-treebanks-v1.1/UD_Danish/da_vsrest-ud-train.conllu"
test = "Universal Dependencies/ud-treebanks-v1.1/UD_Danish/da_vsrest-ud-dev.conllu"

"""
SIZE = [10, 25, 50]
WINDOW = [1, 2, 3]
RETRO = True
LOAD = False
"""
SIZE = [10]
WINDOW = [2]
RETRO = True
LOAD = True

try:
    CREATE = sys.argv[1]
except IndexError:
    raise SystemExit


for size in SIZE:
    for window in WINDOW:

        if CREATE == "y":
            T = Thesis(
                train, test, SIZE=size, LOADMODEL=LOAD, WINDOW=window, RETRO=RETRO)
            LOAD = True
            del T

        path = "Data_vw/UD/"
        t = "-mvectors" + str(size) + ".vw"
        train_vw = path + train.split("/")[-1].replace(".conllu", t)
        test_vw = path + test.split("/")[-1].replace(".conllu", t)

        results = "Results/UD/" + \
            test_vw[11:-21] + "-dev-mvec" + \
            str(size) + "-" + "win" + str(window) + "retro.tsv"
        print results

        """
        #MVEC50 with and without words
        subprocess.call(["hanstholm/build/hanstholm", "--d", train_vw, "--e", test_vw,
                         "--template", "thesis.txt", "--pred", results])
        subprocess.call(["hanstholm/build/hanstholm", "--d", train_vw, "--e", test_vw,
                         "--template", "thesis3.txt", "--pred", results[:-4]+"-nowords.tsv"])
		
"""
        # WALS
        subprocess.call(["hanstholm/build/hanstholm", "--d", train_vw, "--e", test_vw,
                         "--template", "thesis6.txt", "--pred", results[:-4] + "-wals5.tsv"])
"""
        subprocess.call(["hanstholm/build/hanstholm", "--d", train_vw, "--e", test_vw,
                         "--template", "thesis7.txt", "--pred", results[:-4] + "-wals7.tsv"])

    LOAD = False


#Just the baselines
subprocess.call(["hanstholm/build/hanstholm", "--d", train_vw, "--e", test_vw,
                 "--template", "thesis2.txt", "--pred", "Results/UD/" + test_vw[11:-21] + "baseline.tsv"])
subprocess.call(["hanstholm/build/hanstholm", "--d", train_vw, "--e", test_vw,
                 "--template", "thesis4.txt", "--pred", "Results/UD/" + test_vw[11:-21] + "baseline-nowords.tsv"])
"""
