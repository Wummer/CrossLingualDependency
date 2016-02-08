import glob
import codecs
import sys
from itertools import izip



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
	f_toconvert = sorted(glob.glob(PARSER+"/"+DATASET+"/*.tsv"))

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


	if PARSER != "":
		with codecs.open(f[:-4]+".conllu","w") as fil:

			with codecs.open("Original/"+lang+"-"+DATASET+".conllu") as f1, codecs.open(f) as f2:

				for _rest,_head in izip(f1,f2):

					if _rest == "\n":
						print >> fil
						continue

					
					tline1 = _rest.strip().split()
					tline2 = _head.strip().split()
					if DATASET == "UD":
						tline1[5:8] = tline2[5:8]
					else:
						tline1[5:7] = tline2[5:7]

					#tline1[6] = tline2[6]
					#tline1[7] = tline2[6]
					if tline1[3] != tline2[3]:
						print "Not the same", tline1[3], tline2[3]
						print f1,f2


					print >> fil, "\t".join(tline1)

			