import glob
import subprocess
import random
import codecs

random.seed(1)


train1 = list(set(glob.glob(
    "Universal Dependencies/ud-treebanks-v1.1/*/*-ud-train.conllu"))
    - set(glob.glob("Universal Dependencies/ud-treebanks-v1.1/*/*_vsrest-ud-train.conllu")))
dev1 = glob.glob("Universal Dependencies/ud-treebanks-v1.1/*/*-ud-dev.conllu")
test1 = glob.glob("Universal Dependencies/ud-treebanks-v1.1/*/*-ud-test.conllu")


illeagle = ["UD_Basque", "UD_French", "UD_German",
            "UD_Indonesian", "UD_Irish", "UD_Spanish"]

train1.sort()
dev1.sort()
test1.sort()

train,dev,test=[],[],[]
for i in xrange(len(test1)):
	if train1[i].split("/")[2] not in illeagle:
		train.append(train1[i])
		dev.append(dev1[i])
		test.append(test1[i])


print "Beginning conversion of %i different languages" % (len(train))

for i in xrange(len(train)):
    lang = train[i].split("/")[-1].split("-")[0]

    print "Transforming: ", train[i].split("/")[-1].split("-")[0]

    #Fiddling with the training files
    a = train[:i]+train[i+1:]
    true_train = train[i].replace("/"+lang,"/"+lang+"_vsrest")

    with codecs.open(true_train,"w") as outfile:
    	for infilename in a:
    		with codecs.open(infilename)  as infile:
    			outfile.write(infile.read())

    p = subprocess.Popen(["python", "conll_to_vw/conll_to_vw.py", true_train, "Data_vw/UD/" +
                      true_train.split("/")[-1][:-6] + "vw", "--feature-set", "dependency", "--coarse"])
    p.kill()

    # Creating the dev and test file are straightforward
    p = subprocess.Popen(["python", "conll_to_vw/conll_to_vw.py", dev[i], "Data_vw/UD/" +
                      dev[i].split("/")[-1][:-6] + "vw", "--feature-set", "dependency", "--coarse"])
    p.kill()

    p = subprocess.Popen(["python", "conll_to_vw/conll_to_vw.py", test[i], "Data_vw/UD/" +
                      test[i].split("/")[-1][:-6] + "vw", "--feature-set", "dependency", "--coarse"])
    p.kill()

raise SystemExit