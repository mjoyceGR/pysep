#!/usr/bin/env python
import numpy as np
import subprocess
import sys
import glob
import os
#my module
PKG_DIR = os.path.abspath(os.path.dirname(__file__))
head = PKG_DIR.split(PKG_DIR.split('dsep3')[1])[0]
sys.path.append(head+'/pysep/')

import isochrone_suites7 as IS
import time as time
import distribute as dist		
 
i=sys.argv[1] ## give unique job identifier so other control files aren't overwritten!!!

run_dir='run'+str(i)   ## which directory are you in (for parallel purposes)


cont_file  = head + '/nml/cont_'+str(i)+'.nml'
shell_file = head + '/'+run_dir+'/run_'+str(i)+'.sh'
phys_file  = head + '/nml/phys_'+str(i)+'.nml'

atm   = 0.0 		## 5=Phoenix; 0= Eddington, 1= KS (CHECK)
eta_D = 1.0 
ovs   = 0.0
endage= -1.0
NMOD  = 9999.0
asteroseismic=0.0
if asteroseismic:
	FREEOS='TRUE'
else:
	FREEOS='FALSE'

prems_model_dir='' 
mhead='sun'
which_comp='Lovelace'  
output_dir=''  


already_run=glob.glob(head +'/run/out_meridith/*.iso')
#print already_run
#sys.exit()

mass, MLTS, Zin, Yin=np.loadtxt(head+'/pysep/grid_'+str(int(i)+1)+'.dat',usecols=(0,1,2,3),unpack=True)


for star in range(len(mass)):
	mstar=mass[star]
	amlt=MLTS[star]   #1.9258
	zin=Zin[star]	#0.019
	yin=Yin[star]	#0.28

	if float(mstar) < 100.0:
		extant_file=head+'/run/out_meridith/m0' + str('%.1f'%(mstar*100.0))+'.'+mhead+'.'+dist.format(amlt)+'.Z'+dist.format(zin)+'.Y'+ str('%.2f'%(yin))+'.iso'
 	else:
		extant_file=head+'/run/out_meridith/m' + str('%.1f'%(mstar*100.0))+'.'+mhead+'.'+dist.format(amlt)+'.Z'+dist.format(zin)+'.Y'+ str('%.2f'%(yin))+'.iso' 
	print extant_file

	if str(extant_file) in already_run:
 		print 'skpping...this file already exists: ', extant_file
		pass

	else:

		IS.do_run(mstar,amlt,zin,yin, shell_file, cont_file, phys_file, run_dir,atm, eta_D,ovs, FREEOS,NMOD=NMOD, endage=endage,prems_model_dir=prems_model_dir,output_dir=output_dir,model_ID_head=mhead, which_comp=which_comp,asteroseismic=asteroseismic, head=head)


