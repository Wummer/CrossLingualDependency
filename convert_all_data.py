import glob
import subprocess
import random
import codecs
import sys

random.seed(1)


dataset = str(sys.argv[1])

if dataset == "UD":
    train1 = list(set(glob.glob(
        "Universal Dependencies/ud-treebanks-v1.1/*/*-ud-train.conllu"))
        - set(glob.glob("Universal Dependencies/ud-treebanks-v1.1/*/*_vsrest-ud-train.conllu")))
    dev1 = glob.glob(
        "Universal Dependencies/ud-treebanks-v1.1/*/*-ud-dev.conllu")
    test1 = glob.glob(
        "Universal Dependencies/ud-treebanks-v1.1/*/*-ud-test.conllu")

    illeagle = ["UD_Basque", "UD_French", "UD_German",
                "UD_Indonesian", "UD_Irish", "UD_Spanish"]
elif dataset == "SPMRL":
    train1 = list(set(glob.glob("SPMRL mapped/*/*-train5k.conllu")) -
                  set(glob.glob("SPMRL mapped/*/*_vsrest-spmrl-train5k.conllu")))
    test1 = glob.glob("SPMRL mapped/*/*-test.conllu")

    illeagle = []

else:
    print sys.argv[1]
    print "Expected UD or SPMRL as argument 1"
    raise SystemExit

train1.sort()
dev1.sort() if dataset == "UD" else ""
test1.sort()

train, dev, test = [], [], []
for i in xrange(len(test1)):
    if train1[i].split("/")[2] not in illeagle:
        train.append(train1[i])
        dev.append(dev1[i]) if dataset == "UD" else ""
        test.append(test1[i])


print "Beginning conversion of %i different languages" % (len(train))

for i in xrange(len(train)):
    lang = train[i].split("/")[-1].split("-")[0]

    print "Transforming: ", train[i].split("/")[-1].split("-")[0]

    # Fiddling with the training files
    a = train[:i] + train[i + 1:]
    true_train = train[i].replace("/" + lang, "/" + lang + "_vsrest")

    with codecs.open(true_train, "w") as outfile:
        for infilename in a:
            with codecs.open(infilename) as infile:
                for line in infile:
                    outfile.write(line)

    subprocess.call(["python", "conll_to_vw/conll_to_vw.py", true_train, "Data_vw/" + dataset + "/" +
                     true_train.split("/")[-1][:-6] + "vw", "--feature-set", "dependency", "--coarse"])

    # Creating the dev and test file are straightforward
    subprocess.call(["python", "conll_to_vw/conll_to_vw.py", test[i], "Data_vw/" + dataset + "/" +
                     test[i].split("/")[-1][:-6] + "vw", "--feature-set", "dependency", "--coarse"])

    if dataset == "UD":
        subprocess.call(["python", "conll_to_vw/conll_to_vw.py", dev[i], "Data_vw/" + dataset + "/" +
                         dev[i].split("/")[-1][:-6] + "vw", "--feature-set", "dependency", "--coarse"])


raise SystemExit
