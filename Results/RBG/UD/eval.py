from __future__ import division
import glob
import codecs

"""
This file is simply used to calculate UAS / LAS for all .tsv files.
"""

def UAS(eval_file):
	correct=0
	total=0

	for line in codecs.open(eval_file):
		tline = line.strip().split("\t")
		
		if len(tline) < 2:
			continue

		if tline[1].endswith("punct"):
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

		if tline[1].endswith("punct"):
			continue

		if tline[1] == tline[2]:
			correct+=1
		total+=1
	
	return correct/total*100


print "="*20,"UD RESULTS","="*20
print "-"*20,"Dev results","-"*20
for f in sorted(glob.glob("UD/da_vsrest-dev*.tsv")):
	print "Results for",(f[3:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print

print "-"*20,"Baselines","-"*20
for f in sorted(glob.glob("UD/*_vsrest-baseline.tsv")):
	print "Results for",(f[3:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print

print "-"*20,"Baselines with no words","-"*20
for f in sorted(glob.glob("UD/*_vsrest-baseline-nowords.tsv")):
	print "Results for",(f[3:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print

print "-"*20,"MVec25 win1 Retro","-"*20
for f in sorted(glob.glob("UD/*_vsrest--mvec25-win1retro*")):
	print "Results for",(f[3:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print


print "="*20,"SPMRL RESULTS","="*20
print "-"*20,"Baselines","-"*20
for f in sorted(glob.glob("SPMRL/*_vsrest-baseline.tsv")):
	print "Results for",(f[6:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print

print "-"*20,"Baselines with no words","-"*20
for f in sorted(glob.glob("SPMRL/*_vsrest-baseline-nowords.tsv")):
	print "Results for",(f[6:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print

print "-"*20,"MVec25retro","-"*20
for f in sorted(glob.glob("SPMRL/*-mvec25-win1retro*.tsv")):
	print "Results for",(f[6:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print

"""
print "-"*20,"MVec10 win3 Retro","-"*20
for f in sorted(glob.glob("UD/*_vsrest--mvec10-win3retro*")):
	print "Results for",(f[3:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print

print "-"*20,"MVec25 win2 Retro","-"*20
for f in sorted(glob.glob("UD/*_vsrest--mvec25-win2retro*")):
	print "Results for",(f[3:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print


print "-"*20,"MVec25Retro","-"*20
for f in sorted(glob.glob("UD/*-mvec25retrowin2.tsv")):
	print "Results for",(f[3:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print

print "-"*20,"MVec25Retro with no words","-"*20
for f in sorted(glob.glob("UD/*-mvec25retrowin2-nowords.tsv")):
	print "Results for",(f[3:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print

print "-"*20,"MVec50retro","-"*20
for f in sorted(glob.glob("UD/*-mvec50retrowin2.tsv")):
	print "Results for",(f[3:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print

print "-"*20,"MVec50retro with no words","-"*20
for f in sorted(glob.glob("UD/*-mvec50-win2retro-nowords.tsv")):
	print "Results for",(f[3:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print

print "-"*20,"MVec50retro with no words and wals","-"*20
for f in sorted(glob.glob("UD/*mvec50-win2retro-wals.tsv")):
	print "Results for",(f[3:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print


print "-"*20,"MVec Nivre","-"*20
for f in sorted(glob.glob("UD/*-nivre*.tsv")):
	print "Results for",(f[3:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print




print "="*20,"SPMRL RESULTS","="*20
print "-"*20,"Baselines","-"*20
for f in sorted(glob.glob("SPMRL/*baseline.tsv")):
	print "Results for",(f[6:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print

print "-"*20,"Baselines with no words","-"*20
for f in sorted(glob.glob("SPMRL/*baseline-nowords.tsv")):
	print "Results for",(f[6:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print

print "-"*20,"MVec50retro","-"*20
for f in sorted(glob.glob("SPMRL/*-mvec50-win2retro.tsv")):
	print "Results for",(f[6:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print

print "-"*20,"MVec50retro with no words","-"*20
for f in sorted(glob.glob("SPMRL/*-mvec50-win2retro-nowords.tsv")):
	print "Results for",(f[6:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print

print "-"*20,"MVec10retro with no words and wals","-"*20
for f in sorted(glob.glob("SPMRL/*-mvec10-win2retro-wals.tsv")):
	print "Results for",(f[6:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print


print "-"*20,"MVec50retro with no words and wals","-"*20
for f in sorted(glob.glob("SPMRL/*-mvec50-win2retro-wals.tsv")):
	print "Results for",(f[6:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print

print "-"*20,"MVec50retro with no words and wals5","-"*20
for f in sorted(glob.glob("SPMRL/*-mvec50-win2retro-wals5.tsv")):
	print "Results for",(f[6:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print

print "-"*20,"MVec50retro with no words and wals6","-"*20
for f in sorted(glob.glob("SPMRL/*-mvec50-win2retro-wals6.tsv")):
	print "Results for",(f[6:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print

print "-"*20,"Nivre template","-"*20
for f in sorted(glob.glob("SPMRL/*-nivre.tsv")):
	print "Results for",(f[6:])
	print "UAS: ",UAS(f),"%"
	print "LAS: ",LAS(f),"%"
	print

"""