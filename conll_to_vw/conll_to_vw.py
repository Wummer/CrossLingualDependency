# coding: utf-8
"""Create Hanstholm compatible feature files from treebanks
Credit to Anders Johannsen, Post.doc @ CST, KU.

Usage:
  conll_to_vw.py <input> <output> [--feature-set NAME] [--name NAME] [--coarse]
  conll_to_vw.py (-h | --help)

Options:
  -h --help                 Show this screen.
  --feature-set NAME        Which feature to use [default: honnibal13].
  --name NAME               Name of dataset. Output as part of the id for each token [default: d].
  --coarse                  Use coarse-grained tags.
"""
import codecs
from collections import defaultdict
from docopt import docopt
from pos_features import taskar12, honnibal13, honnibal13_groups, dependency, normalize_label, normalize_word

if __name__ == '__main__':
    args = docopt(__doc__)

    data_out = codecs.open(args['<output>'], 'w', encoding='utf-8')
    data_in = codecs.open(args['<input>'], encoding='utf-8')

    features_for_token = {
        'taskar12': taskar12,
        'honnibal13': honnibal13,
        'honnibal13-groups': honnibal13_groups,
        'dependency': dependency
    }[args['--feature-set']]

    def output_sentence(sent):
        label_key = 'cpos' if args['--coarse'] else 'pos'

        if args['--feature-set'] == "dependency":
            for i in xrange(len(sent["word"])):
                try:
                    print >>data_out, u"{label} '{sent_i}-{token_i}{features}".format(
                        label=normalize_label(sent['dependency'][i]),
                        sent_i=sent_i,
                        token_i=i,
                        features=u" ".join(features_for_token(sent['word'], sent[label_key], i)))
                #We need this check for sentences we skip
                except IndexError:
                    continue 

        else:
            for i in xrange(len(sent["word"])):
                print >>data_out, "{label} '{name}-{sent_i}-{token_i}|".format(
                    label=normalize_label(sent[label_key][i]),
                    name=args['--name'],
                    sent_i=sent_i,
                    token_i=i + 1),
                print >>data_out, u" ".join(
                    features_for_token(sent['word'], sent[label_key], i))

    # Process one sentence at a time
    sent = defaultdict(list)
    sent_i = 1
    repeat = False  # used for dependency
    for line in data_in:
        parts = line.strip().split()

        # Comments handling
        if len(parts) > 1 and parts[0].startswith("#") or line.startswith("#"):
            continue

        elif len(parts) >= 10:
            word = parts[1]
            if word.isdigit():
                number = int(word)
                if 1800 <= number <= 2100:
                    word = "!YEAR"
                else:
                    word = "!DIGITS"

            sent['word'].append(word)
            sent['cpos'].append(parts[3])
            sent['pos'].append(parts[4])
            if args['--feature-set'] == "dependency":
                if parts[6] != "_" and parts[7] != "_":
                    # As UD counts root as 0 and hanstholm uses -1 as root we
                    # have to convert to int so we can -1

                    to_append = u"" + str(int(parts[6]) - 1) + "-" + parts[7]
                    # The if statement is for notations such as 2-3, where
                    # there are no morph features. We therefore repeat the
                    # previous statement
                    if repeat:
                        to_append = u"" + \
                            str(int(parts[6]) - 1) + "-" + parts[7]
                        sent['dependency'].append(to_append)
                        repeat = False
                    sent['dependency'].append(to_append)

                elif parts[6] == "_" and parts[7] == "_" and parts[3] == "_" and parts[4] == "_":
                    continue
                    
                else:
                    print "the other case"
                    repeat = True

        elif len(parts) == 0:
            if sent_i > 1:
                print >>data_out, ""
            output_sentence(sent)
            sent_i += 1
            sent = defaultdict(list)

        else:
            print line
            print parts
            raise ValueError("Invalid input format")

    if len(sent['word']):
        output_sentence(sent)
