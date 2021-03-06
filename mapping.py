import codecs
import universal_tags


language = "Polish"
map_dict = {"arabic": "ar", "basque": "ba", "french": "fr", "german": "de", "hebrew": "he",
            "hungarian": "hu", "korean": "ko", "polish": "pl", "swedish": "sv"}

train_file = "SPMRL/SPMRL_SHARED_2014/" + \
    language.upper() + "_SPMRL/gold/conll/train5k/train5k." + \
    language + ".gold.conll"

test_file = "SPMRL/SPMRL_SHARED_2014/" + \
    language.upper() + "_SPMRL/gold/conll/test/test." + \
    language + ".gold.conll"

train_out = "SPMRL mapped/SPMRL_" + language + "/"+map_dict[language.lower()]+"-spmrl-train5k.conllu"
test_out = "SPMRL mapped/SPMRL_" + language + "/"+map_dict[language.lower()]+"-spmrl-test.conllu"


in_ = [train_file, test_file]
out_ = [train_out, test_out]

train_language = train_file.split("_")[2].split("/")[-1].lower()
test_language = test_file.split("_")[2].split("/")[-1].lower()


print train_language

print map_dict[train_language]

a = universal_tags.fileids(map_dict[train_language])
print a
pos_map = universal_tags.mapping(a[0])

print pos_map

for i in xrange(len(in_)):
    with codecs.open(out_[i], "w", "utf-8") as f:
        for line in codecs.open(in_[i], "r", "utf-8"):
            if len(line) > 1:
                tline = line.split("\t")
                tline[3] = pos_map[tline[4]]
                f.write("\t".join(tline))
            else:
                f.write("\n")
