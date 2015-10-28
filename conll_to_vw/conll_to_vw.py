# coding: utf-8
"""Create Hanstholm compatible feature files from treebanks

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

        #if args['--feature-set'] == "dependency":
        for i in xrange(len(sent["word"])):
            print >>data_out, "{label} '{name}-{sent_i}-{token_i}|".format(
                label=normalize_label(sent['dependency'][i]
                                      if args['--feature-set'] == "dependency"
                                      else sent[label_key][i]),
                name=args['--name'],
                sent_i=sent_i,
                token_i=i + 1),
            print >>data_out, u" ".join(
                features_for_token(sent['word'], sent[label_key], i))

    # Process one sentence at a time
    sent = defaultdict(list)
    sent_i = 1
    for line in data_in:
        parts = line.strip().split()

        if len(parts) > 1 and parts[0] == "#":
            continue

        elif len(parts) == 10:
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
            sent['dependency'].append(str(int(parts[6]) - 1) + "-" + parts[7])

        elif len(parts) == 0:
            if sent_i > 1:
                print >>data_out, ""
            output_sentence(sent)
            sent_i += 1
            sent = defaultdict(list)

        else:
            raise ValueError("Invalid input format")

    if len(sent['word']):
        output_sentence(sent)

"""
-1-root '1-0|w call |p VERB |g 0:0.000946125935946 1:0.00115843318564 2:0.00164611628065 3:0.99040
5596025 4:0.0518654057144 5:0.00323278463435 6:-0.000540941484706 7:0.0127166846253 8:0.0010138855
9676 9:0.00151462919182 10:0.000696873548268 11:0.000625316857231 12:0.00122827888005 13:0.0004846
99254127 14:0.00285206378997 15:0.00245394984848 16:0.0054327172697 17:0.000817775603701 18:0.0006
85274226885 19:0.000360483031162 20:0.000407179297901 21:0.00161160153102 22:0.00088030983554 23:0
.0028693018232 24:0.0 25:0.00121155747785 26:0.000313526864102 27:0.000406572976426 28:0.002389942
28043 29:0.000518259912703 30:0.00170511525402 31:0.000396755447007 32:0.000363933090702 33:0.0016
1160153102
"""
