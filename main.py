# define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
import codecs
import logging
import subprocess
import universal_tags
import w2v.word2vec as w2v
import numpy as np
from w2v.sampler import random_sampler, sample_word2vec

from numpy import random

random.seed(1)
np.random.seed(1)
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class Thesis:

    """What I need:

    reading method:
        + UD 
        + SPMRL
    feature creation:
        + fpos vectors
        - baseline
        - competing method
    output to data:
        + vectors

    parser?
        - hanstholm

    """

    def __init__(self, train_file, test_file, DATA="UD", FEAT=True, METHOD="mvectors", P=[0.2, 0.8],SIZE=25,WINDOW=2,WORKERS=4):

        #"Initialized" variables
        self.text = []
        self.cpos = []
        self.fpos = []
        self.all_pos = []
        self.model = []

        # Files
        self.train_file = train_file
        self.test_file = test_file

        # Parameters
        self.DATA = DATA
        self.FEAT = FEAT
        self.METHOD = METHOD
        self.P = P
        self.WINDOW = WINDOW
        self.SIZE = SIZE
        self.WORKERS = WORKERS

        """ DATA """
        
        self.train_cpos,self.train_fpos, self.train_all_pos = self.read_input(train_file)
        self.test_cpos,self.test_fpos, self.test_all_pos = self.read_input(test_file)

        """ FEATURE CREATION """
        self.feature_creation()

        """ ENRICHMENT """
        self.enrichment()

        """ PARSER """

    def read_input(self, file):
        """
        Reads the dataset files and extract the text, cPOS, fPOS and shuffled POS lists.
        Currently only support .conll-x files and dataset as 'UD' or 'SPMRL'.
        """
        f = codecs.open(file)

        text, cpos, fpos = [], [], []
        t_cpos, t_fpos, t_text, all_pos = [], [], [], []

        if self.DATA == "UD" or self.DATA == "SPMRL":
            for line in f:
            # First check if line is not 'empty' and then create our strings
            # text, cpos and fpos
                if line[0] == "#":
                    continue
                    
                elif line != "\n":
                    tline = line.strip("\n").lower().split("\t")

                    t_text.append(tline[1])
                    t_cpos.append(tline[3].replace("|","+"))

                    if tline[4] != "_":
                        t_fpos.append(tline[4].replace("|","+") if self.FEAT== False 
                                else "+".join(sorted(tline[4].split("|"))) + "+" + "+".join(sorted(tline[5].split("|"))))

                    elif tline[4] == "_":
                        t_fpos.append("+".join(sorted(tline[3].split("|")))+ "+" + "+".join(sorted(tline[5].split("|"))))

                    else:
                        raise ValueError("This dataset does not have fPOS. You must set FEAT=True")

                elif line == "\n":
                    all_pos.append(self.shuffle_list(t_fpos,t_cpos))
                    text.append(t_text)
                    cpos.append(t_cpos)
                    fpos.append(t_fpos)
                    t_text, t_cpos, t_fpos = [], [], []

        else:
            raise ValueError(
                "Unknown data set.\nUse UD for Universal Dependencies\n" +
                "or SPMRL for Statistical Parsing of Morphologically Rich Languages")

        return cpos, fpos, all_pos

    def shuffle_list(self, a, b):
        """shuffle_list(a,b) takes two lists as input.
        Then shuffles the list such that each index element from a
         is followed by the same index element from b
        """
        c = [None] * (len(a) + len(b))
        c[::2] = a
        c[1::2] = b
        return c

    def feature_creation(self, METHOD="mvectors"):
        vectors = []
        if METHOD == "mvectors":
            model = w2v.Word2Vec(
                self.train_all_pos, context=True, min_count=0, sampler=random_sampler,
                size=self.SIZE, workers=self.WORKERS, window=self.WINDOW, p=self.P)
            self.model = model

            """ 
            ############## DO I EVEN NEED MORE? ####################
            """
        else:
            raise ValueError("Unknown method. Did you mean 'mvectors'?")

    def enrichment(self):

        if self.DATA == "UD":
            train = "Data_vw/UD/" + self.train_file.split("/")[-1][:-7] + ".vw"
            test = "Data_vw/UD/" + self.test_file.split("/")[-1][:-7] + ".vw"
        
        write_files = [train,test]
        read_files = [self.train_file,self.test_file]
        pos = [self.train_fpos,self.test_fpos]

        for idx in xrange(len(write_files)):
            with codecs.open(write_files[idx][:-3] + ("-feats" if self.FEAT==True else "")+ "-mvectors.vw", "w") as f:
                sent_tracker = 0
                idx_tracker = 0
                for line in codecs.open(write_files[idx]):
                    if line == "\n":
                        sent_tracker += 1
                        idx_tracker = 0
                        print >> f
                        continue

                    try:
                        vec = self.model[pos[idx][sent_tracker][idx_tracker]]
                        tline = line[:-1] + "|g " + " ".join(
                            str(x) + ":" + str(y) for x, y in enumerate(vec))
                        print >> f, tline
                    except KeyError:
                        print >> f, line.strip("\n")
                    finally:
                        idx_tracker += 1