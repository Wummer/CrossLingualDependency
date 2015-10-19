
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


def read_conll(file):
    f = codecs.open(file)
    text = []
    cpos = []
    fpos = []
    sentence_no = 0

    t_cpos = []
    t_fpos = []
    t_text = []
    all_pos = []

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
                # adding the line count at the end of each sentenc
            # t_fpos.append(sentence_no)
            # sentence_no+=1
            all_pos.append(shuffle_list(t_fpos, t_cpos))
            text.append(t_text)
            cpos.append(t_cpos)
            fpos.append(t_fpos)
            t_text, t_cpos, t_fpos = [], [], []

    return text, cpos, fpos, all_pos

    f.close()


def shuffle_list(a, b):
    """
    Takes 2 lists as input and returns a single shuffled list.
    Each index element from the first list is followed by the index element of the other list.
    """
    c = [None] * (len(a) + len(b))
    c[::2] = a
    c[1::2] = b

    return c
#if __name__ == "__main__":
train, cpos, fpos, both_pos = read_conll(eng_data)

print both_pos[0]

model = w2v.Word2Vec(
    both_pos, context=True, min_count=0, sampler=random_sampler, workers=4, size=10)


print model.most_similar(["nnp"])
print model["nn"]
print model['noun']
