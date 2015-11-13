from __future__ import division
import glob
import codecs


def UAS(eval_file):
	correct=0
	total=0

	for line in codecs.open(eval_file):
		tline = line.strip().split("\t")
		
		if len(tline) < 2:
			continue


		if tline[1].split("-")[0] == tline[2].split("-")[0]:
			correct+=1

		total+=1

	return correct/total*100


def LAS(eval_file):
	correct=0
	total=0

	for line in codecs.open(eval_file):
		tline = line.strip().split("\t")
		if len(tline) < 2:
			continue

		if tline[1] == tline[2]:
			correct+=1
		total+=1
	
	return correct/total*100

print "="*20,"UD RESULTS","="*20
print "-"*20,"Baselines","-"*20
for f in sorted(glob.glob("UD/*-baseline.tsv")):
	print "Results for",(f.split("-")[0][3:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print



print "-"*20,"MVec25","-"*20
print "Results for MVecFeats25 on UD_Bulgarian:"
print "UAS: ",UAS("UD/bg_vsrest-ud-feats-mvectors-25.tsv"),"%"
print "LAS: ",LAS("UD/bg_vsrest-ud-feats-mvectors-25.tsv"),"%"