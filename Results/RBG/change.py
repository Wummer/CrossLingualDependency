import glob
import codecs
from itertools import izip





f_toconvert = sorted(glob.glob("SPMRL/*.out"))

for f in f_toconvert:
	lang = f.split("_")[0][-2:]

	with codecs.open(f[:-4]+".conllu","w") as fil:

		with codecs.open("Original/"+lang+".conllu") as f1, codecs.open(f) as f2:

			for _rest,_head in izip(f1,f2):

				if _rest == "\n":
					print >> fil
					continue
				
				tline1 = _rest.strip().split()
				tline2 = _head.strip().split()
				tline1[5:8] = tline2[5:8]
				#tline1[6] = tline2[6]
				#tline1[7] = tline2[6]
				if tline1[3] != tline2[3]:
					print "Not the same", tline1[3], tline2[3]


				print >> fil, "\t".join(tline1)

			