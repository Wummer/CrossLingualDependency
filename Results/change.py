import glob
import codecs
import sys
from itertools import izip
import numpy as np

np.random.seed(2)



try:
	DATASET = sys.argv[1]
except IndexError:
	print "change requires SPMRL or UD as argument"
	raise SystemExit

try:
	PARSER = sys.argv[2]
except IndexError:
	PARSER=""

if PARSER != "":
	f_toconvert = sorted(glob.glob(PARSER+"/"+DATASET+"/*.out"))
else:
	f_toconvert = sorted(set(glob.glob(DATASET+"/*.tsv"))-set(glob.glob(DATASET+"/*dev*.tsv")))

for f in f_toconvert:
	lang = f.split("_")[0][-2:]
	if lang == "fi":
		if len(f.split("_")) ==3:
			lang = "fi_ftb"

	with codecs.open("Original/"+DATASET+"-"+lang+".conllu") as f1:
		with codecs.open("Original/"+lang+"-"+DATASET+".conllu","w") as f2:
			for line in f1: 
				if line.startswith("#"):
					continue
				elif line == "\n":
					print >> f2
				elif "-" in line.split()[0]:
					continue
				else:
					print >> f2, line.strip()



	with codecs.open(f[:-4]+".conllu","w") as fil:

		with codecs.open("Original/"+lang+"-"+DATASET+".conllu") as f1, codecs.open(f) as f2:

			pos = 0
			neg = 0
			for _rest,_head in izip(f1,f2):

				if _rest == "\n" or "":
					print >> fil
					continue

				if PARSER != "":
					tline1 = _rest.strip().split()
					tline2 = _head.strip().split()
					if DATASET == "UD":
						tline1[5:8] = tline2[5:8]
					else:
						tline1[5:7] = tline2[5:7]

					if tline1[3] != tline2[3]:
						print "Not the same", tline1[3], tline2[3]
						print f1,f2

				else:
					tline1 = _rest.strip().split()
					cnt,real,pred = _head.strip().split("\t")

					if real.replace("-","|",1).split("|")[0] != pred.replace("-","|",1).split("|")[0]:
						randint = np.random.choice([-1,1])
						if randint == 1:
							pos+=1
						else:
							neg+=1
						tline1[6] = str(int(tline1[6])+randint)

					if real.replace("-","|",1).split("|")[1] != pred.replace("-","|",1).split("|")[1]:
						tline1[7] = pred.replace("-","|",1).split("|")[1]

					tline1[5] = "_"



				print >> fil, "\t".join(tline1)
			print pos, neg

	# Added that last line in a trivial way
	if PARSER == "":
		with codecs.open(f[:-4]+".conllu","a") as fil:
			print >> fil

		