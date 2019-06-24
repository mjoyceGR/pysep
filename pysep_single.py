#!/usr/bin/env python
import numpy as np
import subprocess
import sys
import os
#my module
PKG_DIR = os.path.abspath(os.path.dirname(__file__))
head = PKG_DIR.split('run')[0]
sys.path.append(head+'pysep/')

import isochrone_suites6 as IS
import time as time
		
#################################################################################################
#################################################################################################

#WARNING: MAY NEED TO EXPORT FREEOS PATH BEFORE EXECUTION:

#################################################################################################
#################################################################################################
prems=True

i=27 			## give unique job identifier so other control files aren't overwritten!!!
run_dir='run'   ## which directory are you in (for parallel purposes)


cont_file  = head + '/nml/cont_'+str(i)+'.nml'
shell_file = head + '/'+run_dir+'/run_'+str(i)+'.sh'
phys_file  = head + '/nml/phys_'+str(i)+'.nml'

mstar = 1.0
amlt  = 1.9258   
zin   = 0.014	
yin   = 0.27	 

atm   = 5 		## 5=Phoenix; 0= Eddington, 1= KS (CHECK)
eta_D = 1.0
ovs   = 0.0
endage= -1 #0.48  #Gyr

NMOD  = 9999
asteroseismic=False

if asteroseismic:
	FREEOS='TRUE'
else:
	FREEOS='FALSE' ##FREEOS="TRUE"  ## for sophisticated pulsation compatibility, this must be set to true...?

#######################################################################
#
# Generate all pre-main sequence models in serial FIRST
# to avoid thread copying/compilation issues of poly executable
#
########################################################################
prems_model_dir='alpha_cen'#'betaHydri_prems'
mhead='alpha_cen'#'betaHydri'
which_comp='Lovelace'
output_dir=''

print "head", head

if prems:

 	IS.make_prems_models(mstar,amlt,zin,yin,\
 	model_ID_head=mhead, which_comp=which_comp,\
 	model_dir=prems_model_dir, head=head)
	print "\n\npre-main sequence collection generated!"

else:
	print "have you made your pre-main sequence models?"	
	time.sleep(2)


IS.do_run(          mstar,amlt,zin,yin,\
                    shell_file, cont_file, phys_file, run_dir,\
                    atm, eta_D,ovs, FREEOS,\
	 				NMOD=NMOD, endage=endage,\
	 				prems_model_dir=prems_model_dir,\
	 				output_dir=output_dir,\
	 				model_ID_head=mhead, which_comp=which_comp,\
	 				asteroseismic=asteroseismic, head = head)
