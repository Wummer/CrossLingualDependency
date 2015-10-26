
import codecs
import logging
import subprocess
import w2v.word2vec as w2v
from w2v.sampler import random_sampler, sample_word2vec
import numpy as np
from numpy import random

# define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

eng_data = "Universal Dependencies/ud-treebanks-v1.1/UD_English/en-ud-train.conllu"
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

    def __init__(self, input_file, DATA="UD", METHOD="mvectors", P=[]):
        self.input_file = input_file

        self.text = []
        self.cpos = []
        self.fpos = []
        self.all_pos = []

        """ DATA """
        if DATA == "UD":
            read_UD(input_file)
        elif DATA == ""SPMRL:
            read_SPMRL(input_file):
        else:
            raise ValueError(
                "Unknown data set.Use UD for Universal Dependencies" +
                " or SPMRL for Statistical Parsing of Morphologically Rich Languages")

        """ METHOD """

        """ ENRICHMENT """

        """ PARSER """

    def read_UD(self, file):
        """
        Read the Universal Dependencies files and extract the text, cPOS, fPOS and shuffled POS lists.
        """
        f = codecs.open(file)

        text, cpos, fpos = [], [], []
        t_cpos, t_fpos, t_text, all_pos = [], [], [], []

        for line in f:

            # First check if line is not 'empty' and then create our strings of
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
                all_pos.append(shuffle_list(t_fpos, t_cpos))
                text.append(t_text)
                cpos.append(t_cpos)
                fpos.append(t_fpos)
                t_text, t_cpos, t_fpos = [], [], []

        self.text = text
        self.cpos = cpos
        self.fpos = fpos
        self.all_pos = all_pos

        # return text, cpos, fpos, all_pos

        f.close()

    def read_SPMRL(self, file):
        f = codecs.open(file)

        text, cpos, fpos = [], [], []

    def shuffle_list(self, a, b):
        c = [None] * (len(a) + len(b))
        c[::2] = a
        c[1::2] = b
        return c

# if __name__ == "__main__":
train, cpos, fpos, both_pos = read_conll(eng_data)

print both_pos[0]

model = w2v.Word2Vec(
    both_pos, context=True, min_count=0, sampler=random_sampler, workers=4, size=10)


print model.most_similar(["nnp"])
print model["nn"]
print model['noun']
