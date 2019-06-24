#!/usr/bin/env python
import numpy as np
import subprocess
import sys
import os
PKG_DIR = os.path.abspath(os.path.dirname(__file__))
head = PKG_DIR.split(PKG_DIR.split('dsep3')[1])[0]
sys.path.append(head+'/pysep/')

###########################################
#
# NEW isochrone_suites version 6/24/19
#
##########################################
import isochrone_suites7 as IS
import generate_prems7 as GP
import time as time

def format(number):
	number=float(number)
	f=("%.3f"%number)
	return f

def makegrid(grid_file, m_centroid, mlt_centroid, z_centroid, y_centroid, *args, **kwargs):
#######################################################################
#
# make explicit grid
#
#######################################################################

	mrange=float(kwargs.get("mrange",0.2))
	mltrange=float(kwargs.get("mltrange",0.8))
	zrange=float(kwargs.get("zrange",0.012))	
	yrange=float(kwargs.get("yrange",0.12))

	delta_m=float(kwargs.get("delta_m",0.01))
	delta_mlt=float(kwargs.get("delta_mlt",0.01))
	delta_z=float(kwargs.get("delta_z", 0.002))
	delta_y=float(kwargs.get("delta_y", 0.02))

	m_min=m_centroid-mrange/2.0
	m_max=m_centroid+mrange/2.0

	a_min=mlt_centroid-mltrange/2.0
	a_max=mlt_centroid+mltrange/2.0

	z_min=z_centroid-zrange/2.0
	z_max=z_centroid+zrange/2.0
	
	y_min=y_centroid-yrange/2.0
	y_max=y_centroid+yrange/2.0


	mass=np.arange(m_min,m_max,delta_m) ##distributed
	MLTS=np.arange(a_min,a_max,delta_mlt) 					#1.9258 # don't vary?
	Zin=np.arange(z_min,z_max,delta_z)	 #up to 0.019 now  0.017
	Yin=np.arange(y_min,y_max,delta_y) 		 #0.24	

	outf=open(grid_file,"w")#('../pysep/grid_'+str(indx)+'.dat', "w")

	counter =0
	for m in range(len(mass)):
		mstar=format(mass[m])
		for a in range(len(MLTS)):
			amlt=format(MLTS[a])
			for i in range(len(Zin)):
				zin=format(Zin[i])
				for j in range(len(Yin)):
					yin=format(Yin[j])
					print >> outf,  mstar, "   ",amlt,"   ", zin,"   ", yin
					counter = counter +1
	print "there are", counter, " distinct parameter combinations, proceed?"
	time.sleep(1)
	outf.close()
	return 


def scatter_jobs(infile, n):
	#######################################################################
	#
	# subdivide explicit grid across n data files
	#
	#######################################################################
	inf=open(infile,"r")
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
	return 


def print_pysep(name_of_pysep_script,head,\
 				atm, eta_D, ovs, endage,\
 				NMOD, asteroseismic,\
 				prems_model_dir,mhead,which_comp,output_dir):
	
	outf=open(name_of_pysep_script,"w")

	print >> outf, "#!/usr/bin/env python"
	print >> outf, "import numpy as np"
	print >> outf, "import subprocess"
	print >> outf, "import sys"
	print >> outf, "import glob"
	print >> outf, "import os"
	print >> outf, "#my module"
	print >> outf, "PKG_DIR = os.path.abspath(os.path.dirname(__file__))"
	print >> outf, "head = PKG_DIR.split(PKG_DIR.split('dsep3')[1])[0]"
	print >> outf, "sys.path.append(head+'/pysep/')"
	print >> outf, ""
	print >> outf, "import isochrone_suites7 as IS"
	print >> outf, "import time as time"
	print >> outf, "import distribute as dist		"
	print >> outf, " "
	print >> outf, "i=sys.argv[1] ## give unique job identifier so other control files aren't overwritten!!!"
	print >> outf, ""
	print >> outf, "run_dir='run'+str(i)   ## which directory are you in (for parallel purposes)"
	print >> outf, ""
	print >> outf, ""
	print >> outf, "cont_file  = head + '/nml/cont_'+str(i)+'.nml'"
	print >> outf, "shell_file = head + '/'+run_dir+'/run_'+str(i)+'.sh'"
	print >> outf, "phys_file  = head + '/nml/phys_'+str(i)+'.nml'"
	print >> outf, ""
	print >> outf, "atm   = "+ str(float(atm)) +" 		## 5=Phoenix; 0= Eddington, 1= KS (CHECK)"
	print >> outf, "eta_D = "+ str(float(eta_D)) +" "
	print >> outf, "ovs   = "+ str(float(ovs)) +""
	print >> outf, "endage= "+ str(float(endage)) +"" #0.48  #Gyr"
	print >> outf, "NMOD  = "+ str(float(NMOD)) +""
	print >> outf, "asteroseismic="+str(float(asteroseismic))+""
	print >> outf, "if asteroseismic:"
	print >> outf, "	FREEOS='TRUE'"
	print >> outf, "else:"
	print >> outf, "	FREEOS='FALSE'"
	print >> outf, ""
	print >> outf, "prems_model_dir='"+ prems_model_dir +"' "
	print >> outf, "mhead='"+ mhead +"'"
	print >> outf, "which_comp='"+ which_comp+"'  "
	print >> outf, "output_dir='"+ output_dir+"'  "
	print >> outf, ""
	print >> outf, ""
	print >> outf, "already_run=glob.glob(head +'/run/out_meridith/"+output_dir+"*.iso')"
	print >> outf, "#print already_run"
	print >> outf, "#sys.exit()"
	print >> outf, ""
	print >> outf, "mass, MLTS, Zin, Yin=np.loadtxt(head+'/pysep/grid_'+str(int(i)+1)+'.dat',usecols=(0,1,2,3),unpack=True)"
	print >> outf, ""
	print >> outf, ""
	print >> outf, "for star in range(len(mass)):"
	print >> outf, "	mstar=mass[star]"
	print >> outf, "	amlt=MLTS[star]   #1.9258"
	print >> outf, "	zin=Zin[star]	#0.019"
	print >> outf, "	yin=Yin[star]	#0.28"
	print >> outf, ""
	print >> outf, "	if float(mstar) < 100.0:"
	print >> outf, "		extant_file=head+'/run/out_meridith"+output_dir+"/m0' + str('%.1f'%(mstar*100.0))+'.'+mhead+'.'+dist.format(amlt)+'.Z'+dist.format(zin)+'.Y'+ str('%.2f'%(yin))+'.iso'"
	print >> outf, " 	else:"
	print >> outf, "		extant_file=head+'/run/out_meridith"+output_dir+"/m' + str('%.1f'%(mstar*100.0))+'.'+mhead+'.'+dist.format(amlt)+'.Z'+dist.format(zin)+'.Y'+ str('%.2f'%(yin))+'.iso' "
	print >> outf, "	print extant_file"
	print >> outf, ""
	print >> outf, "	if str(extant_file) in already_run:"
	print >> outf, " 		print 'skpping...this file already exists: ', extant_file"
	print >> outf, "		pass"
	print >> outf, ""
	print >> outf, "	else:"
	print >> outf, ""
	print >> outf, "		IS.do_run(mstar,amlt,zin,yin, shell_file, cont_file, phys_file, run_dir,atm, eta_D,ovs, FREEOS,NMOD=NMOD, endage=endage,prems_model_dir=prems_model_dir,output_dir=output_dir,model_ID_head=mhead, which_comp=which_comp,asteroseismic=asteroseismic, head=head)"
	print >> outf, ""
	print >> outf, ""

	outf.close()
	return 




def copy_pysep(name_of_pysep_script,n):
	#######################################################################
	#
	# make a run directory for each thread
	#
	#######################################################################
	print "name of pysep script: ", head+"/pysep/"+name_of_pysep_script
	#sys.exit()
	for i in range(0,n+1):
		subprocess.call("mkdir "+head+"/run"+str(i), shell=True)
		subprocess.call("cp "+head+"/pysep/"+name_of_pysep_script+"  "+head+"/run"+str(i)+"/"+name_of_pysep_script, shell=True)
	return 



def make_all_prems_first(grid_file, mhead, which_comp, prems_model_dir, head):

	print "value of head (loc 2): ", head

	#######################################################################
	#
	# Generate all pre-main sequence models in serial FIRST to avoid thread copying/compilation issues of poly executable
	#
	########################################################################
	mass, MLTS, Zin, Yin=np.loadtxt(grid_file,usecols=(0,1,2,3),unpack=True)
	for star in range(len(mass)):
		#print "new\n--------------------------------------------------------------"
		mstar=mass[star]
		amlt=MLTS[star]   #1.9258
		zin=Zin[star]	#0.019
		yin=Yin[star]	#0.28
	 	
	 	IS.make_prems_models(mstar,amlt,zin,yin,\
	 					model_ID_head=mhead,which_comp=which_comp,\
	 					model_dir=prems_model_dir, head=head)

	print "\n\nMain sequence collection generated!"
	time.sleep(1)