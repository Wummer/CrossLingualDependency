

def create_lexicon(cpos,fpos):
    lex = {}

    for i in xrange(len(cpos)):
        c = cpos[i]
        f  = fpos[i]

        try: 
            lex[c]
        except KeyError:
            lex[c] = [c,f]
        try:
            lex[f]
        except KeyError:
            lex[f] = [f,c]

        if f not in lex[c]:
            lex[c].append(f)
        if c not in lex[c]:
            lex[c].append(c)
        if f not in lex[f]:
            lex[f].append(f)
        if c not in lex[f]:
            lex[f].append(c)

    print lex


fpos = [1,2,3,4,5,6,7]
cpos = ["a","a","b","c","a","d","e"]

create_lexicon(cpos,fpos)