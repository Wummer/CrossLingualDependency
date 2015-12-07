from numpy import random

""" Default word2vec sampler """
def sample_word2vec(sentence, window=5):
    pairs = []
    for i in range(len(sentence)):
        word = sentence[i]
        if word is None:
            continue
        reduced_window = random.randint(window)
        j = i - window + reduced_window

        if j < 0:
            j = 0
        k = i + window + 1 - reduced_window
        if k > len(sentence):
            k = len(sentence)
        for j in range(j, k):
            if j == i or sentence[j] is None:
                continue
            pairs.append((sentence[i], sentence[j]))

    #logging.info("{} samples generated from len {} sentence".format(len(pairs), len(sentence)))

    return pairs


""" My "random" cPOS/fPOS sampler """
def random_sampler(sentence, window=1,p=[0.2,0.8]):
    pairs = []
    context = sentence[1::2]
    sentence = sentence[::2]
    for i in xrange(len(sentence)):
        word = sentence[i]
        if word is None:
            continue
        reduced_window = random.randint(window)
        j = i - window + reduced_window

        if j < 0:
            j = 0
        k = i + window + 1 - reduced_window
        if k > len(sentence):
            k = len(sentence)
        for j in range(j, k):
            if j == i or sentence[j] is None:
                continue
            pairs.append((sentence[i],
             randomizer(sentence[j],context[j],p)))

    #logging.info("{} samples generated from len {} sentence".format(len(pairs), len(sentence)))

    return pairs

"""@randomizer takes 3 inputs:
 - sentence | the current sentence of cPOS
 - index    | the index of the sentence
 - fpos     | the corresponding fPOS list   

 returns either the original cPOS  or the corresponding fPOS at the index. 
"""
def randomizer(word,context,p):
    choice = random.choice([0,1],p=p)
    if choice == 0:
        return word
    elif choice == 1:
        return context