
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
#en_output = "Data/en-ud-train.vw"

random.seed(1)
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class Thesis:

    """What I need:

    reading method:
        + UD 
        + SPMRL
    feature creation:
        - fpos vectors
        - baseline
        - competing method
    output to data:
        - vectors

    parser?
        - hanstholm

    """

    def __init__(self, train_file, test_file, DATA="UD", METHOD="mvectors", P=[0.8,0.2]):
        
        #"Initialized" variables
        self.text = []
        self.cpos = []
        self.fpos = []
        self.all_pos = []
        self.model = []

        #Files
        self.train_file = train_file
        self.test_file = test_file
        
        #Parameters
        self.DATA = DATA
        self.METHOD = METHOD
        self.P = P




        """ DATA """
        self.read_input(train_file, DATA)

        """ FEATURE CREATION """
        #self.feature_creation()

        """ ENRICHMENT """
        self.enrichment()

        """ PARSER """

    def read_input(self, file, dataset):
        """
        Reads the dataset files and extract the text, cPOS, fPOS and shuffled POS lists.
        Currently only support .conll-x files and dataset as 'UD' or 'SPMRL'.
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
        """shuffle_list(a,b) takes two lists as input.
        Then shuffles the list such that each index element from a
         is followed by the same index element from b
        """
        c = [None] * (len(a) + len(b))
        c[::2] = a
        c[1::2] = b
        return c

    def feature_creation(self, METHOD="mvectors", size=10, workers=4):

        vectors = []
        if METHOD == "mvectors":
            model = w2v.Word2Vec(
                self.all_pos, context=True, min_count=0,sampler=random_sampler,
                workers=workers, size=size,p=self.P)
            self.model = model

            """ 
            ############## NEEDS TO BE IMPLEMENTED ####################
            """
        else:
            raise ValueError("Unknown method. Did you mean 'mvectors'?")

    def enrichment(self):

        if self.DATA == "UD":
            train_out = "Data_vw/UD/"+self.train_file[-18:-6]+"vw"
            test_out = "Data_vw/UD/"+self.test_file[-17:-6]+"vw"
            print train_out,test_out



        "blah blah"


"""
train, cpos, fpos, both_pos = read_conll(eng_data)

print both_pos[0]

model = w2v.Word2Vec(
    both_pos, context=True, min_count=0, sampler=random_sampler, workers=4, size=10)
"""
T1 = Thesis(en_train,en_test)