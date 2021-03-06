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

    """What I have done:

    reading method:
        + UD 
        + SPMRL
    feature creation:
        + fpos vectors
        + baseline
        - competing method
    output to data:
        + vectors

    parser
        + hanstholm

    """

    def __init__(self, train_file, test_file, DATA="UD",
                 METHOD="mvectors", LOADMODEL=False, P=[0.2, 0.8],
                 SIZE=25, WINDOW=2, WORKERS=4, RETRO=True, ITER=10, RBG=False):
        
        """ 
        Here we 'initialize' all relevant variables and run the methods. 
        """

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
            train_file.replace("_vsrest",""),WALS=False) #Don't want no 



        """ FEATURE CREATION """
        self.feature_creation()
        if RETRO == True:
            self.retro_feature(ITER)


        """ ENRICHMENT """
        if not RBG:
            self.enrichment()
        else:
            self.RBGenrichment()


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

                    if tline[6] == "_" and tline[7] == "_" and tline[3] == "_" and tline[4] == "_":
                        continue

                    if WALS:
                        t_a81.append(tline[10]) #81a
                        t_a85.append(tline[11]) #85a
                        t_a86.append(tline[12]) #86a
                        t_a87.append(tline[13]) #87a

                    t_text.append(tline[1])
                    t_cpos.append(tline[3].replace("|", "+"))

                    if tline[4] != "_":
                        if self.DATA == "UD":
                            try:
                                t_fpos.append(tline[4].replace("|", "+").split(",")[0]+"+"+tline[14])
                            except IndexError:
                                lang = file.split("/")[-1][:2]
                                t_fpos.append(tline[4].replace("|", "+").split(",")[0]+"+"+lang)
                        else:
                            try:
                                t_fpos.append(tline[4].replace("|", "+")+"+"+tline[14])
                            except IndexError:
                                lang = file.split("/")[-1][:2]
                                t_fpos.append(tline[4].replace("|", "+")+"+"+lang)
                        
                        #if self.FEAT == False
                        #              else "+".join(sorted(tline[4].split("|"))) +
                        #              "+" + "+".join(sorted(tline[5].split("|"))))
                        
                    elif tline[4] == "_":
                        t_fpos.append(
                            "+".join(sorted(tline[3].split("|"))).split(",")[0] +
                            "+" + "+".join(sorted(tline[5].split("|"))))

                    else:
                        raise ValueError(
                            "This dataset does not have fPOS or features.")

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
        lexicon = self.create_lexicon(self.train_cpos+self.embed_cpos,self.train_fpos+self.embed_fpos)
        wordVecs = self.read_word_vecs(self.MODELFILE)
        
        self.model = self.retrofit(wordVecs, lexicon, ITER)
        full_vocab = np.array([self.model[x] for x in self.model.keys()])
        self.min_vector = full_vocab.min(axis=0)
        self.max_vector = full_vocab.max(axis=0)
        self.mean_vector = full_vocab.mean(axis=0)

    def create_WALSvectors(self,pos, vector):
        lang = pos[-2:]
        WALSvector = [pos]+vector.tolist()
        
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

        if lang not in WALS.keys():
            vec = np.zeros(self.SIZE*8).tolist()
            WALSvector += vec

        else:
        #Here we increase the vector size for 
            for feat in WALS[lang]:

                #81a features:
                if feat == "81a_svo":
                    WALSvector += vector
                else:
                    WALSvector += np.zeros(self.SIZE).tolist()
                if feat == "81a_sov":
                    WALSvector += vector
                else:
                    WALSvector += np.zeros(self.SIZE).tolist()

                #85a features:
                if feat == "85a_prep":
                    WALSvector += vector
                else:
                    WALSvector += np.zeros(self.SIZE).tolist()

                if feat == "85a_post":
                    WALSvector += vector
                else:
                    WALSvector += np.zeros(self.SIZE).tolist()

                #86a
                if feat == "86a_gn":
                    WALSvector += vector
                else:
                    WALSvector +=np.zeros(self.SIZE).tolist()

                if feat == "86a_ng":
                    WALSvector += vector
                else:
                    WALSvector += np.zeros(self.SIZE).tolist()

                #87a
                if feat == "87a_na":
                    WALSvector += vector
                else:
                    WALSvector += np.zeros(self.SIZE).tolist()

                if feat == "87a_an":
                    WALSvector += vector
                else:
                    WALSvector += np.zeros(self.SIZE).tolist()

        return WALSvector


    def enrichment(self):
        """
        Enriches the .vw files with the appropriate vectors and WALS features.
        As we can define which features the use in the parser template we just write everything to the file. 
        """

        train = "Data_vw/"+self.DATA+"/" + self.train_file.split("/")[-1][:-7] + ".vw"
        test = "Data_vw/"+self.DATA+"/" + self.test_file.split("/")[-1][:-7] + ".vw"


        fpos_count,cpos_count,all_count=0,0,0
        used_fpos=[]

        #The files we loop over
        write_files = [train, test]

        #read_files = [self.train_file, self.test_file]
        

        pos = [self.train_fpos, self.test_fpos]
        cpos = [self.train_cpos, self.test_cpos]
        wals_feats = [self.train_wals,self.test_wals]




        for idx in xrange(len(write_files)):
            with codecs.open(write_files[idx][:-3]
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
                            """
                            #| g_81a vso0:0 .. | g_81a sov0:0 .. |
                            feat_head, feat_tail = feat[sent_tracker][word_tracker].split("_")
                            tline += " |g_" + feat_head +" "+ " ".join(
                                feat_tail + str(x) + ":" + str(y) for x, y in enumerate(vec))
                            """
                            
                             #| g_81a_vso 0:0 ..| g_81a_sov 0:0 ..|
                            tline += " |g_"+feat[sent_tracker][word_tracker] + " " + " ".join(
                                str(x) + ":" + str(y) for x, y in enumerate(vec))
                            
                            """
                            #|g_81a vso | g_81a sv0|
                            feat_head, feat_tail = feat[sent_tracker][word_tracker].split("_")
                            tline += " |g_" + feat_head + " " + feat_tail 
                            """
                        except IndexError:
                            #Debugging
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


    def RBGenrichment(self):
        "wooptido"

        train_out = "Data_RBG/"+self.DATA+"/"+self.train_file.split("/")[-1].replace(".conllu","-rbg.conllu")
        test_out ="Data_RBG/"+self.DATA+"/"+self.test_file.split("/")[-1].replace(".conllu","-rbg.conllu")

        vec_file = "Vectors/RBG/" + self.DATA + "/" + "mvectors" + str(self.SIZE) + "-win" + str(self.WINDOW) + "retro"
        lang = []


        read_files = [self.train_file,self.test_file]
        write_files = [train_out, test_out]

        pos = [self.train_fpos, self.test_fpos]
        cpos = [self.train_cpos, self.test_cpos]
        wals_feats = [self.train_wals,self.test_wals]

        #Here we print the retotrofitted vector to a file we can use in RBGparser
        with codecs.open(vec_file,"w") as f:
            for _pos,vec in self.model.iteritems():
                #vec = (vec - self.min_vector) / self.max_vector * 1e-4 
                line_out = _pos.replace("|","+") + " " + " ".join(str(x) for x in vec) 
                print  >> f, line_out
            print >> f, "*UNKNOWN*" + " " + " ".join(str(x) for x in self.model["x"])

        with codecs.open(vec_file+"-wals","w") as f:
            for _pos,vec in self.model.iteritems():
                WALSvec = self.create_WALSvectors(_pos.replace("|","+"), vec)
                #vec = (vec - self.min_vector) / self.max_vector * 1e-4 
                line_out = " ".join(str(x) for x in WALSvec)
                print  >> f, line_out

            print >> f, "*UNKNOWN*" + " " + " ".join(str(x) for x in self.model["x"]*8)


        for idx in xrange(len(write_files)):

            #Our basic model in the works!
            with codecs.open(write_files[idx][:-7]
                             + "-mvectors" + str(self.SIZE) + ".conllu","w") as f:

                for line in codecs.open(read_files[idx]):
                    if line == "\n":
                        print >> f
                        continue

                    if line.startswith("#"):
                        continue

                    
                    tline = line.strip().split()
                    if tline[6] == "_" and tline[7] == "_" and tline[3] == "_" and tline[4] == "_":
                        continue 

                    try:
                        tline[1] = tline[4]+"+"+tline[14]
                    except IndexError:
                        tline[1] = tline[4]+"+"+read_files[idx].split("/")[-1][:2]
                    tline[2] = "_"
                    tline[4] = "_"
                    tline[5] = "_"

                    if self.DATA == "SPMRL":
                        tline[7] = "_"
                    tline = tline[:-5]
                    print >> f, "\t".join(tline)

            #Our model with lemmas in the works!
            lang_idx = 0
            with codecs.open(write_files[idx][:-7]
                             + "-mvectors" + str(self.SIZE) + "-lemma.conllu","w") as f:

                for line in codecs.open(read_files[idx]):
                    if line == "\n":
                        print >> f
                        continue

                    if line.startswith("#"):
                        continue

                    
                    tline = line.strip().split()
                    if tline[6] == "_" and tline[7] == "_" and tline[3] == "_" and tline[4] == "_":
                        continue

                    try:
                        tline[1] = tline[4]+"+"+tline[14]
                    except IndexError:
                        tline[1] = tline[4]+"+"+read_files[idx].split("/")[-1][:2]
                    tline[4] = "_"
                    tline[5] = "_"
                    if self.DATA == "SPMRL":
                        tline[7] = "_"
                    tline = tline[:-5]
                    lang_idx +=1
                    print >> f, "\t".join(tline)

            #WALS goes here whenever ...
            with codecs.open(write_files[idx][:-7]
                             + "-mvectors" + str(self.SIZE) + "-wals.conllu","w") as f:

                for line in codecs.open(read_files[idx]):
                    if line == "\n":
                        print >> f
                        continue

                    if line.startswith("#"):
                        continue

                    
                    tline = line.strip().split()
                    if tline[6] == "_" and tline[7] == "_" and tline[3] == "_" and tline[4] == "_":
                        continue

                    try:
                        tline[1] = tline[4]+"+"+tline[14]
                    except IndexError:
                        tline[1] = tline[4]+"+"+read_files[idx].split("/")[-1][:2] 
                    tline[2] = "_"
                    tline[4] = "_"
                    tline[5] = "_"
                    if self.DATA == "SPMRL":
                        tline[7] = "_"

                    """
                    for feat in tline[-5:-1]:
                        try:
                            vec = self.model[tline[1].lower().strip()]
                        except KeyError:
                            vec = self.model["x"]

                        tline[5] += feat + " " + " ".join(str(x) for x in vec)
                    """ 
                    #WALS as words
                    #tline[5] = "|".join(tline[-4:])

                    """
                    if tline[5] == "_":
                        tline[5] = "|".join(tline[-4:])
                    else:
                        tline[5] += "|" + "|".join(tline[-4:])
                    """
                    tline = tline[:-5]
                    print >> f, "\t".join(tline)

            #Baseline-nowords in the making:
            with codecs.open(write_files[idx][:-7]+ "-baseline-nowords.conllu","w") as f:
                for line in codecs.open(read_files[idx]):
                    if line == "\n":
                        print >> f
                        continue

                    if line.startswith("#"):
                        continue
                    

                    #Baseline-nowords in the making:
                    tline = line.strip().split()
                    if tline[6] == "_" and tline[7] == "_" and tline[3] == "_" and tline[4] == "_":
                        continue

                    tline[1] = "_"
                    tline[2] = "_"
                    tline[4] = "_"
                    tline[5] = "_"
                    if self.DATA == "SPMRL":
                        tline[7] = "_"
                    tline = tline[:-5]
                    print >> f, "\t".join(tline)

            #Baseline with words and all that jazz
            with codecs.open(write_files[idx][:-7]+ "-baseline.conllu","w") as f:
                for line in codecs.open(read_files[idx]):
                    if line == "\n":
                        print >> f
                        continue

                    if line.startswith("#"):
                        continue
                    #Baseline-nowords in the making:
                    tline = line.strip().split()
                    if tline[6] == "_" and tline[7] == "_" and tline[3] == "_" and tline[4] == "_":
                        continue
                        
                    tline[5] = "_"
                    tline[4] = "_"
                    if self.DATA == "SPMRL":
                        tline[7] = "_"
                    tline = tline[:-5]
                    print >> f, "\t".join(tline)

    def create_lexicon(self,cpos,fpos):
        """
        Creates the lexicon needed for retrofitting. 
        It follows the template of the lexicon files contained in the original retrofitting script.
        """
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
    The following functions are taken from the Retrofitting repo and slightly modified to fit my class. 
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
