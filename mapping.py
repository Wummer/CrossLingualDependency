import codecs
import universal_tags

def map_to_universal(line):
	map_path = "universal-pos-tags/"


#OK: German, 
train_file="SPMRL/SPMRL_SHARED_2014/HUNGARIAN_SPMRL/gold/conll/train/train.Hungarian.gold.conll"
test_file="SPMRL/SPMRL_SHARED_2014/HUNGARIAN_SPMRL/gold/conll/train/test.Hungarian.gold.conll"


train_language = train_file.split("_")[2].split("/")[-1].lower()
test_language = test_file.split("_")[2].split("/")[-1].lower()


print train_language
map_dict = {"arabic" : "ar", "basque" : "ba", "french" : "fr", "german" : "de", "hebrew"  : "he", 
"hungarian" : "hu", "korean" : "ko", "polish" : "pl", "sweden" : "sv"}
print map_dict[train_language]

a = universal_tags.fileids(map_dict[train_language])
print a
pos_map = universal_tags.mapping(a[0])

print pos_map

for line in codecs.open(train_file):
	if len(line)>1:
		tline= line.split("\t")
		print tline
		print tline[3],tline[4],pos_map[tline[4]]
	else: print 