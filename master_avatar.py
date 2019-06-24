#!/usr/bin/env python
import numpy as np
import subprocess
import sys
import os
import codecs
#my module
#sys.path.append('/marsha/mjoyce/dsep3/pysep/')
sys.path.append('/avatar/mjoyce/dsep3/pysep/')

###########################################
#
# NEW isochrone_suites version 2/20/19
#
##########################################
import isochrone_suites6 as IS
import generate_prems6 as GP

import time as time


makegrid=True
make_run_dirs=True
prems=False



n=496#56 #number of threads

def format(number):
	number=float(number)
	f=("%.3f"%number)
	return f

#######################################################################
#
# make explicit grid
#
#######################################################################
if makegrid:
	mass=np.arange(1.0,1.21,0.01) ##distributed
	MLTS=np.arange(1.6,2.01,0.01) 					#1.9258 # don't vary?
	Zin=np.arange(0.014,0.026,0.002)	 #up to 0.019 now  0.017
	Yin=np.arange(0.22,0.34,0.02) 		 #0.24	

	outf=open("wholegrid.dat","w")#('../pysep/grid_'+str(indx)+'.dat', "w")

	counter =0
	for m in range(len(mass)):
		mstar=format(mass[m])
		for a in range(len(MLTS)):
			amlt=format(MLTS[a])
			for i in range(len(Zin)):
				zin=format(Zin[i])
				for j in range(len(Yin)):
					yin=format(Yin[j])
					print >> outf, mstar, "   ",amlt,"   ", zin,"   ", yin
					counter = counter +1
	print "there are", counter, " distinct parameter combinations"
	outf.close()


#######################################################################
#
# subdivide explicit grid across n data files
#
#######################################################################
inf=open("wholegrid.dat","r")
section_size=float(len(inf.readlines()))/float(n)  #WARNING integer division 
section_size=int(np.floor(section_size))
inf.seek(0)

lines=[]
for line in inf:
	lines.append(line)


lower_bound=0
upper_bound=section_size
for i in range(0,n):
	with open('../pysep/grid_'+str(i+1)+'.dat', "w") as f:
		if i == n-1:
			print "i = n-1", i, n-1
			for entry in lines[lower_bound:]:
				f.write(entry)
		else:
			for entry in lines[lower_bound:upper_bound]:
				f.write(entry)

		lower_bound=upper_bound + 1
		upper_bound=lower_bound + section_size
#sys.exit()



#######################################################################
#
# make a run directory for each thread
#
#######################################################################
if make_run_dirs:
	# for i in range(0,n+1):
	# 	try:
	# 		subprocess.call("mkdir /avatar/mjoyce/dsep3/run"+str(i), shell=True)
	# 	except:
	# 		pass

	for i in range(0,n+1):
		subprocess.call("cp /avatar/mjoyce/dsep3/pysep/flexpysep.py /avatar/mjoyce/dsep3/run"+str(i)+"/flexpysep.py", shell=True)




#######################################################################
#
# Generate all pre-main sequence models in serial FIRST to avoid thread copying/compilation issues of poly executable
#
########################################################################
prems_model_dir='betaHydri_prems'
mhead='betaHydri'
which_comp='AVATAR'

if prems:
	mass, MLTS, Zin, Yin=np.loadtxt('wholegrid.dat',usecols=(0,1,2,3),unpack=True)
	for star in range(len(mass)):
		#print "new\n--------------------------------------------------------------"
		mstar=mass[star]
		amlt=MLTS[star]   #1.9258
		zin=Zin[star]	#0.019
		yin=Yin[star]	#0.28
	 	
	 	IS.make_prems_models(mstar,amlt,zin,yin,\
	 					model_ID_head=mhead,which_comp=which_comp, model_dir=prems_model_dir)

	print "\n\nMain sequence collection generated!"
else:
	print "have you made your pre-main sequence models?"	
	time.sleep(5)