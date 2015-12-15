from __future__ import division
import codecs
import logging
import subprocess
import universal_tags
import w2v.word2vec as w2v
import numpy as np
import argparse
import gzip
import math
import numpy
import re
import sys

from copy import deepcopy
from w2v.sampler import random_sampler, sample_word2vec
from numpy import random


# define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

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

    def __init__(self, train_file, test_file, DATA="UD", FEAT=False,
                 METHOD="mvectors", LOADMODEL=False, P=[0.2, 0.8], SIZE=25, WINDOW=2, WORKERS=4,RETRO=True,ITER=10):

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
        self.LOADMODEL = LOADMODEL

        self.MODELFILE = "Vectors/" + \
                self.train_file.split("/")[-1][:-7] + str(self.SIZE) + "win" + str(WINDOW)

        # Settings
        self.isNumber = re.compile(r'\d+.*')

        self.wo_Dict = {}

        """ DATA """

        self.train_cpos, self.train_fpos, self.train_all_pos, self.train_wals = self.read_input(
            train_file)
        self.test_cpos, self.test_fpos, self.test_all_pos, self.test_wals = self.read_input(
            test_file)
        self.embed_cpos, self.embed_fpos, self.embed_all_pos = self.read_input(
            train_file.replace("_vsrest",""),WALS=False)



        """ FEATURE CREATION """
        self.feature_creation()
        if RETRO == True:
            self.retro_feature(ITER)


        """ ENRICHMENT """
        self.enrichment()


        """ PARSER """

    def read_input(self, file, WALS=True):
        """
        Reads the dataset files and extract the text, cPOS, fPOS and shuffled POS lists.
        Currently only support .conll-x files and dataset as 'UD' or 'SPMRL'.
        """
        f = codecs.open(file)

        text, cpos, fpos = [], [], [],
        t_cpos, t_fpos, t_text, all_pos, = [], [], [], []

        #WALS features
        a81, a85, a86, a87 = [],[],[],[]
        t_a81, t_a85, t_a86, t_a87 = [],[],[],[]

        if self.DATA == "UD" or self.DATA == "SPMRL":
            for line in f:
            # First check if line is not 'empty' and then create our strings
            # text, cpos and fpos
                if line[0] == "#":
                    continue

                elif line != "\n":
                    tline = line.strip("\n").lower().split()

                    if WALS:
                        t_a81.append(tline[10])
                        t_a85.append(tline[11])
                        t_a86.append(tline[12])
                        t_a87.append(tline[13])

                    t_text.append(tline[1])
                    t_cpos.append(tline[3].replace("|", "+"))

                    if tline[4] != "_":
                        t_fpos.append(tline[4].replace("|", "+") and tline[4].split(",")[0] if self.FEAT == False
                                      else "+".join(sorted(tline[4].split("|"))) +
                                      "+" + "+".join(sorted(tline[5].split("|"))))

                    elif tline[4] == "_":
                        t_fpos.append(
                            "+".join(sorted(tline[3].split("|"))).split(",")[0] +
                            "+" + "+".join(sorted(tline[5].split("|"))))

                    else:
                        raise ValueError(
                            "This dataset does not have fPOS. You must set FEAT=True")

                elif line == "\n":
                    if WALS:
                        a81.append(t_a81)
                        a85.append(t_a85)
                        a86.append(t_a86)
                        a87.append(t_a87)
                        t_a81, t_a85, t_a86, t_a87 = [],[],[],[]


                    all_pos.append(self.shuffle_list(t_fpos, t_cpos))
                    text.append(t_text)
                    cpos.append(t_cpos)
                    fpos.append(t_fpos)
                    t_text, t_cpos, t_fpos = [], [], []

        else:
            raise ValueError(
                "Unknown data set.\nUse UD for Universal Dependencies\n" +
                "or SPMRL for Statistical Parsing of Morphologically Rich Languages")
        if WALS:
            return cpos,fpos,all_pos, [a81,a85,a86,a87]

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
        """
        Utilizes the modified word2vec model to create vectors 
        """
        vectors = []
        if METHOD == "mvectors":
            if self.LOADMODEL == True:
                model = w2v.Word2Vec.load_word2vec_format(self.MODELFILE)
            else:
                model = w2v.Word2Vec(
                    self.train_all_pos+self.embed_all_pos, context=True, min_count=0, sampler=random_sampler,
                    size=self.SIZE, workers=self.WORKERS, window=self.WINDOW, p=self.P)
                model.save_word2vec_format(self.MODELFILE)
            self.model = model
            full_vocab = np.array([self.model[x] for x in self.model.vocab.keys()])
            self.min_vector = full_vocab.min(axis=0)
            self.max_vector = full_vocab.max(axis=0)

            """ 
            ############## DO I EVEN NEED MORE? ####################
            """
        else:
            raise ValueError("Unknown method. Did you mean 'mvectors'?")

    def retro_feature(self,ITER):
        """
        Applies retrofitting to the vectors.
        """
        lexicon = self.create_lexicon(self.train_cpos,self.train_fpos)
        wordVecs = self.read_word_vecs(self.MODELFILE)
        
        self.model = self.retrofit(wordVecs, lexicon, ITER)
        full_vocab = np.array([self.model[x] for x in self.model.keys()])
        self.min_vector = full_vocab.min(axis=0)
        self.max_vector = full_vocab.max(axis=0)


    def enrichment(self):

        train = "Data_vw/"+self.DATA+"/" + self.train_file.split("/")[-1][:-7] + ".vw"
        test = "Data_vw/"+self.DATA+"/" + self.test_file.split("/")[-1][:-7] + ".vw"


        fpos_count,cpos_count,all_count=0,0,0
        used_fpos=[]

        #The files we loop over
        write_files = [train, test]
        read_files = [self.train_file, self.test_file]
        pos = [self.train_fpos, self.test_fpos]
        cpos = [self.train_cpos, self.test_cpos]
        wals_feats = [self.train_wals,self.test_wals]

        for idx in xrange(len(write_files)):
            with codecs.open(write_files[idx][:-3] + ("-feats" if self.FEAT == True else "")
                             + "-mvectors" + str(self.SIZE) + ".vw", "w") as f:
                sent_tracker = 0
                word_tracker = 0
                for line in codecs.open(write_files[idx]):
                    if line == "\n":
                        sent_tracker += 1
                        word_tracker = 0
                        print >> f
                        continue
                    #Only interested in test scenario
                    if idx>0:
                        all_count +=1

                    try:
                        vec = (self.model[pos[idx][sent_tracker][
                               word_tracker]] - self.min_vector) / self.max_vector * 1e-4
                        if idx>0:
                            fpos_count+=1
                            #if pos[idx][sent_tracker] not in used_fpos:
                            #    used_fpos.append(pos[idx][sent_tracker])
                    except KeyError:
                        vec = (self.model[cpos[idx][sent_tracker][
                            word_tracker]] - self.min_vector) / self.max_vector * 1e-4
                        if idx>0:
                            cpos_count+=1                        

                    tline = line[:-1] + " |g " + " ".join(
                        str(x) + ":" + str(y) for x, y in enumerate(vec))

                    # Adding the WALS features per Dr. phil Soegaard!
                    for feat in wals_feats[idx]:
                        try:
                            
                            tline += " |g_" + feat[sent_tracker][word_tracker] +" "+ " ".join(
                                str(x) + ":" + str(y) for x, y in enumerate(vec))
        
                            """
                            tline += " "+feat[sent_tracker][word_tracker] + ":" + " ".join(
                                str(x) + ":" + str(y) for x, y in enumerate(vec))
                            """
                        except IndexError:
                            print line
                            print tline
                            print pos[idx][sent_tracker],len(pos[idx][sent_tracker])
                            print feat[sent_tracker], len(feat[sent_tracker])
                            raise SystemExit


                    print >> f, tline
                    #Only interested in test scenario

                    word_tracker += 1

        print all_count,"pos tags were parsed"
        print "Of these",fpos_count,"were fPOS and",cpos_count,"were cPOS"


    def create_lexicon(self,cpos,fpos):
        lex = {}

        for l in xrange(len(cpos)):
            for i in xrange(len(cpos[l])):
                c = cpos[l][i]
                f  = fpos[l][i]

                try: 
                    lex[c]
                except KeyError:
                    lex[c] = [f]
                try:
                    lex[f]
                except KeyError:
                    lex[f] = [c]

                if f not in lex[c]:
                    lex[c].append(f)
                if c not in lex[f]:
                    lex[f].append(c)

        return lex


    """
    The following functions are taken from the Retrofitting repo and modified to fit my class. 
    All credits go to Manaal Faruqui, mfaruqui@cs.cmu.edu
    """

    def norm_word(self, word):
        if self.isNumber.search(word.lower()):
            return '---num---'
        elif re.sub(r'\W+', '', word) == '':
            return '---punc---'
        else:
            return word.lower()

    ''' Read all the word vectors and normalize them '''

    def read_word_vecs(self, filename):
        wordVectors = {}
        if filename.endswith('.gz'):
            fileObject = gzip.open(filename, 'r')
        else:
            fileObject = open(filename, 'r')

        for line in fileObject:
            if len(line.split()) < self.SIZE+1:
                continue
            line = line.strip().lower()
            word = line.split()[0]
            wordVectors[word] = numpy.zeros(len(line.split()) - 1, dtype=float)
            for index, vecVal in enumerate(line.split()[1:]):
                wordVectors[word][index] = float(vecVal)
            ''' normalize weight vector '''
            wordVectors[word] /= math.sqrt((wordVectors[word]**2).sum() + 1e-6)

        sys.stderr.write("Vectors read from: " + filename + " \n")
        return wordVectors

    ''' Write word vectors to file '''

    def print_word_vecs(self, wordVectors, outFileName):
        sys.stderr.write('\nWriting down the vectors in ' + outFileName + '\n')
        outFile = open(outFileName, 'w')
        for word, values in wordVectors.iteritems():
            outFile.write(word + ' ')
            for val in wordVectors[word]:
                outFile.write('%.4f' % (val) + ' ')
            outFile.write('\n')
        outFile.close()

    ''' Read the PPDB word relations as a dictionary '''

    def read_lexicon(self, filename, wordVecs):
        lexicon = {}
        for line in open(filename, 'r'):
            words = line.lower().strip().split()
            lexicon[norm_word(words[0])] = [norm_word(word)
                                            for word in words[1:]]
        return lexicon

    ''' Retrofit word vectors to a lexicon '''

    def retrofit(self, wordVecs, lexicon, numIters):
        newWordVecs = deepcopy(wordVecs)
        wvVocab = set(newWordVecs.keys())
        loopVocab = wvVocab.intersection(set(lexicon.keys()))
        for it in range(numIters):
            # loop through every node also in ontology (else just use data
            # estimate)
            for word in loopVocab:
                wordNeighbours = set(lexicon[word]).intersection(wvVocab)
                numNeighbours = len(wordNeighbours)
                # no neighbours, pass - use data estimate
                if numNeighbours == 0:
                    continue
                # the weight of the data estimate if the number of neighbours
                newVec = numNeighbours * wordVecs[word]
                # loop over neighbours and add to new vector (currently with
                # weight 1)
                for ppWord in wordNeighbours:
                    newVec += newWordVecs[ppWord]
                newWordVecs[word] = newVec / (2 * numNeighbours)
        return newWordVecs
"""
if __name__=='__main__':

  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--input", type=str, default=None, help="Input word vecs")
  parser.add_argument("-l", "--lexicon", type=str, default=None, help="Lexicon file name")
  parser.add_argument("-o", "--output", type=str, help="Output word vecs")
  parser.add_argument("-n", "--numiter", type=int, default=10, help="Num iterations")
  args = parser.parse_args()

  wordVecs = read_word_vecs(args.input)
  lexicon = read_lexicon(args.lexicon, wordVecs)
  numIter = int(args.numiter)
  outFileName = args.output
  
  ''' Enrich the word vectors using ppdb and print the enriched vectors '''
  print_word_vecs(retrofit(wordVecs, lexicon, numIter), outFileName) 

"""
