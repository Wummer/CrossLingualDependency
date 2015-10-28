
import codecs
import logging
import subprocess
import w2v.word2vec as w2v
from w2v.sampler import random_sampler, sample_word2vec
import numpy as np
from numpy import random

# define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

en_train = "Universal Dependencies/ud-treebanks-v1.1/UD_English/en-ud-train.conllu"
en_test = "Universal Dependencies/ud-treebanks-v1.1/UD_English/en-ud-test.conllu"

random.seed(1)
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class Thesis:

    """What I need:

    reading method:
        + UD 
        - SPMRL
    feature creation:
        - fpos vectors
        - baseline
        - competing method
    output to data:
        - vectors

    parser?
        - hanstholm

    """

    def __init__(self, train_file, test_file, output_file, DATA="UD", METHOD="mvectors", P=[]):
        self.train_file = train_file

        self.text = []
        self.cpos = []
        self.fpos = []
        self.all_pos = []
        self.model = []

        """ DATA """
        self.read_input(train_file, DATA)

        """ FEATURE CREATION """
        self.feature_creation()

        """ ENRICHMENT """

        """ PARSER """

    def read_input(self, file, dataset):
        """
        Read the Universal Dependencies files and extract the text, cPOS, fPOS and shuffled POS lists.
        """
        f = codecs.open(file)

        text, cpos, fpos = [], [], []
        t_cpos, t_fpos, t_text, all_pos = [], [], [], []

        if dataset == "UD":
            for line in f:
            # First check if line is not 'empty' and then create our strings
            # text, cpos and fpos
                if line != "\n":
                    tline = line.strip("\n").strip().lower().split("\t")

                    if t_text == [] and t_cpos == [] and t_fpos == []:
                        t_text.append(tline[1])
                        t_cpos.append(tline[3])
                        t_fpos.append(tline[4])
                    else:
                        t_text.append(tline[1])
                        t_cpos.append(tline[3])
                        t_fpos.append(tline[4])

                if line == "\n":
                    all_pos.append(self.shuffle_list(t_fpos, t_cpos))
                    text.append(t_text)
                    cpos.append(t_cpos)
                    fpos.append(t_fpos)
                    t_text, t_cpos, t_fpos = [], [], []

        elif dataset == "SPMRL":
            for line in f:

                if line != "\n":
                    tline = line.strip("\n").strip().lower().split("\t")

                    if t_text == [] and t_cpos == [] and t_fpos == []:
                        t_text.append(tline[1])
                        t_cpos.append(tline[3])
                        t_fpos.append(
                            tline[4] + "+" + tline[5].replace("|", "+"))

                if line == "\n":
                    all_pos.append(self.shuffle_list(t_fpos, t_cpos))
                    text.append(t_text)
                    cpos.append(t_cpos)
                    t_text, t_cpos, t_fpos = [], [], []

        else:
            raise ValueError(
                "Unknown data set.Use UD for Universal Dependencies" +
                " or SPMRL for Statistical Parsing of Morphologically Rich Languages")

        self.text = text
        self.cpos = cpos
        self.fpos = fpos
        self.all_pos = all_pos

        # return text, cpos, fpos, all_pos

        f.close()

    def shuffle_list(self, a, b):
        c = [None] * (len(a) + len(b))
        c[::2] = a
        c[1::2] = b
        return c

    def feature_creation(self, METHOD="mvectors", size=10, workers=4):

        vectors = []
        if METHOD == "mvectors":
            model = w2v.Word2Vec(
                self.all_pos, context=True, min_count=0,sampler=random_sampler,
                workers=workers, size=size,p=P)
            self.model = model

            """ 
            ############## NEEDS TO BE IMPLEMENTED ####################
            """
        else:
            raise ValueError("Unknown method. Did you mean 'mvectors'?")

    def enrichment(self,train_file,test_file):

        f = codecs.open(train_file)
        f1 = codecs.open(test_file)

        for line in f:
            



        "blah blah"


"""
train, cpos, fpos, both_pos = read_conll(eng_data)

print both_pos[0]

model = w2v.Word2Vec(
    both_pos, context=True, min_count=0, sampler=random_sampler, workers=4, size=10)
"""
T1 = Thesis(eng_data)

print T1.fpos[10]
print T1.model["nnp"]
print T1.model.most_similar("nn")