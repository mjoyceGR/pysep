#!/usr/bin/env python
import numpy as np
import subprocess
import sys
import os
import codecs
import glob
#my module
#sys.path.append('/marsha/mjoyce/dsep3/pysep/')
sys.path.append('/avatar/mjoyce/dsep3/pysep/')


subprocess.call("rm catch",shell=True)
subprocess.call("touch catch",shell=True)


#outf=open("catch", "a")
for f in glob.glob("grid_*.dat"):
	inf=open(f, "r")
	#lines=[]
	for line in inf:
		print line
		#lines.append(line)

		#for line in lines:
			#subprocess.call("grep "+str(line)+ " *.dat", shell=True)
		#subprocess.call("'"+ (line)+ "'  >> catch",shell=True)	
		#print >> outf, line
		subprocess.call("grep '"+ (line)+ "' *.dat | wc >> catch",shell=True)# stdout=subprocess.PIPE)
		#print >> outf, "\n"
		#subprocess.call(" '   '  >> catch",shell=True)
			#output = proc.stdout.read()
			#print output

	inf.seek(0)
	inf.close()

#outf.close()