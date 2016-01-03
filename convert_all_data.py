import glob
import subprocess
import random
import codecs
import sys

random.seed(1)

# Initializer
try:
    dataset = str(sys.argv[1])
except IndexError:
    print "Must have argument 1 as SPMRL or UD"

try:
    if str(sys.argv[2]) == "subsample":
        subsample=True
except IndexError:
    subsample=False

def create_WALS_files(train, true_train,subsample):
    with codecs.open(true_train, "w+") as outfile:
        for infilename in train:
            with codecs.open(infilename) as infile:
                for line in infile:
                    if line == "\n":
                        print >> outfile
                    else:
                        tline = line.strip("\n")
                        tline += " " + " ".join(WALS[lang])
                        print >> outfile, tline


# Loading of the data
if dataset == "UD":
    train1 = list(set(glob.glob(
        "Universal Dependencies/ud-treebanks-v1.1/*/*-ud-train.conllu"))
        - set(glob.glob("Universal Dependencies/ud-treebanks-v1.1/*/*_vsrest-ud-train.conllu")))
    dev1 = list(set(glob.glob(
        "Universal Dependencies/ud-treebanks-v1.1/*/*-ud-dev.conllu")) -
        set(glob.glob("Universal Dependencies/ud-treebanks-v1.1/*/*_vsrest-ud-dev.conllu")))
    test1 = list(set(glob.glob(
        "Universal Dependencies/ud-treebanks-v1.1/*/*-ud-test.conllu")) -
        set(glob.glob("Universal Dependencies/ud-treebanks-v1.1/*/*_vsrest-ud-test.conllu")))

    illeagle = ["UD_Basque", "UD_French", "UD_German",
                "UD_Indonesian", "UD_Irish", "UD_Spanish"]

elif dataset == "SPMRL":

    train1 = list(set(glob.glob("SPMRL mapped/*/*-train5k.conllu")) -
                  set(glob.glob("SPMRL mapped/*/*_vsrest-spmrl-train5k.conllu")))

    test1 = list(set(glob.glob("SPMRL mapped/*/*-test.conllu")) -
                 set(glob.glob("SPMRL mapped/*/*_vsrest-spmrl-test.conllu")))
    illeagle = [""]

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

# WALS features

WALS = {"bg": ["81a_svo", "85a_prep", "86a_none", "87a_an"],
        "hr": ["81a_svo", "85a_prep", "86a_none", "87a_an"],
        "cs": ["81a_svo", "85a_prep", "86a_gn", "87a_an"],
        "da": ["81a_svo", "85a_prep", "86a_none", "87a_an"],
        "en": ["81a_svo", "85a_prep", "86a_none", "87a_an"],
        "fi": ["81a_svo", "85a_post", "86a_gn", "87a_an"],
        "fi_ftb": ["81a_svo", "85a_post", "86a_gn", "87a_an"],
        "el": ["81a_none", "85a_prep", "86a_ng", "87a_an"],
        "he": ["81a_svo", "85a_prep", "86a_ng", "87a_na"],
        "hu": ["81a_none", "85a_post", "86a_gn", "87a_an"],
        "it": ["81a_svo", "85a_prep", "86a_ng", "87a_na"],
        "fa": ["81a_sov", "85a_prep", "86a_ng", "87a_na"],
        "sv": ["81a_svo", "85a_prep", "86a_gn", "87a_an"],
        "fr": ["81a_svo", "85a_prep", "86a_ng", "87a_na"],
        "de": ["81a_none", "85a_prep", "86a_ng", "87a_an"],
        "pl": ["81a_svo", "85a_prep", "86a_ng", "87a_an"],
        }

print "Beginning conversion of %i different languages" % (len(train))

for i in xrange(len(train)):
    lang = train[i].split("/")[-1].split("-")[0]

    print "Transforming: ", lang

    # Fiddling with the training files
    a = train[:i] + train[i + 1:]
    true_train = train[i].replace("/" + lang, "/" + lang + "_vsrest")

    # Creating _vsrest files and adding WALS features
    create_WALS_files(a, true_train,subsample)

    # Now adding test features
    true_test = test[i].replace("/" + lang, "/" + lang + "_vsrest")

    create_WALS_files([test[i]], true_test,subsample)

    if dataset == "UD":
        true_dev = dev[i].replace("/" + lang, "/" + lang + "_vsrest")

        create_WALS_files([dev[i]], true_dev,subsample)

    subprocess.call(["python", "conll_to_vw/conll_to_vw.py", true_train, "Data_vw/" + dataset + "/" +
                     true_train.split("/")[-1][:-6] + "vw", "--feature-set", "dependency", "--coarse"])

    # Creating the dev and test file are straightforward
    subprocess.call(["python", "conll_to_vw/conll_to_vw.py", true_test, "Data_vw/" + dataset + "/" +
                     true_test.split("/")[-1][:-6] + "vw", "--feature-set", "dependency", "--coarse"])

    if dataset == "UD":
        subprocess.call(["python", "conll_to_vw/conll_to_vw.py", true_dev, "Data_vw/" + dataset + "/" +
                         true_dev.split("/")[-1][:-6] + "vw", "--feature-set", "dependency", "--coarse"])


raise SystemExit
