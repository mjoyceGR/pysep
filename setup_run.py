#!/usr/bin/env python
import numpy as np
import subprocess
import sys
import os
PKG_DIR = os.path.abspath(os.path.dirname(__file__))
head = PKG_DIR.split(PKG_DIR.split('dsep3')[1])[0]
sys.path.append(head+'pysep/')
import distribute as dist

grid_name="lovelace_test_grid.dat"
n=36

m=1.0
mlt=1.9
z=0.014
y=0.27

mrange= 0.05
mltrange= 1.0  
zrange= 0.02
yrange=0.1


delta_m=0.01
delta_mlt=0.1
delta_z=0.001
delta_y=0.01



atm   = 0 				## 5=Phoenix; 0= Eddington, 1= KS (CHECK)
eta_D = 1.0
ovs   = 0.0
endage= -1 				#0.48  #Gyr
NMOD  = 9999
asteroseismic=False


prems_model_dir='' #'procyon'
mhead='sun'#'procyon'
which_comp='Lovelace'
output_dir=''


dist.makegrid(grid_name,\
			  m, mlt, z, y,\
			  mrange=mrange,\
			  mltrange=mltrange,\
			  zrange=zrange,\
			  yrange=yrange,\
			  delta_m=delta_m,\
			  delta_mlt=delta_mlt,\
			  delta_z=delta_z,\
			  delta_y=delta_y)

dist.scatter_jobs(grid_name,n)


name_of_pysep_script = 'test_pysep.py'

dist.print_pysep(name_of_pysep_script,head,\
 				 atm, eta_D, ovs, endage,\
 				 NMOD, asteroseismic,\
 				 prems_model_dir, mhead,which_comp, output_dir)


dist.copy_pysep(name_of_pysep_script,n)

#dist.make_all_prems_first(grid_name, mhead, which_comp, prems_model_dir, head)