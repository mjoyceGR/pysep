#!/usr/bin/env python
import numpy as np
import subprocess
import sys
import codecs
import re as re
import shutil
import os
import sys, os, time
from subprocess import Popen, list2cmdline

header='/home/mjoyce/dsep3/'
sys.path.append(header+'pysep/')
sys.path.append('/home/mjoyce/dsep3/pysep/')
import generate_prems6 as GP 


# solar_ML = 1.9258 ##new as of 4/5/17
# Zsolar=0.019
# Ysolar=0.28
# aFe=0.0
###########################################################################################

def cpu_count():
    ''' Returns the number of CPUs in the system
    '''
    num = 1
    if sys.platform == 'win32':
        try:
            num = int(os.environ['NUMBER_OF_PROCESSORS'])
        except (ValueError, KeyError):
            pass
    elif sys.platform == 'darwin':
        try:
            num = int(os.popen('sysctl -n hw.ncpu').read())
        except ValueError:
            pass
    else:
        try:
            num = os.sysconf('SC_NPROCESSORS_ONLN')
        except (ValueError, OSError, AttributeError):
            pass    
    print "number of threads available: ", num
    return num


def exec_commands(cmds):
    ''' Exec commands in parallel in multiple process 
    (as much as we have CPU)
    '''
    if not cmds: return # empty list
    def done(p):
        return p.poll() is not None
    def success(p):
        return p.returncode == 0
    def fail():
        sys.exit(1)

    max_task = cpu_count()
    processes = []
    while True:
        while cmds and len(processes) < max_task:
            task = cmds.pop()
            #task = task + ""
            print list2cmdline(task)
            processes.append(Popen(  task , stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True ))

        for p in processes:
            if done(p):
            	print "process ", p, " believes it has concluded successfully...."
                if success(p):
                    processes.remove(p)
                else:
                	print "process ", p, "has failed"
                	#fail()
                	pass

        if not processes and not cmds:
            break
        else:
            time.sleep(0.05)

def format(number):
	number=float(number)
	f=("%.3f"%number)
	return f

#####################################################################################
def update_cont(cont_file, CMIXLA, Z, Y,NMOD, *args, **kwargs):
	endage=float(kwargs.get('endage',-4.7))
	#which_comp=str(kwargs.get('which_comp','LMC'))
	head = str(kwargs.get('head', ''))


	# if which_comp=='LMC':
	# 	comp_str='mjoyce'
	# else:
	# 	comp_str='mjoyce'
	asteroseismic=bool(kwargs.get('asteroseismic',False))
	

	cont=open(cont_file,"w")	
	# def strip_DSEP_header(in_file, outfn, *args, **kwargs):
	# mjoyce_common.py:	n = int(kwargs.get('n', 14))

	Z_solar=0.019
	X = 1.00-float(Y)-float(Z)


	print >> cont, " $CONTROL"
	print >> cont, " DESCRIP(1)='[Fe/H]=0.0'"
	print >> cont, " DESCRIP(2)='mjoyce_on_LMC' "
	print >> cont, ""
	print >> cont, " NUMRUN=2"
	print >> cont, ""
	print >> cont, " KINDRN(1)=2"
	print >> cont, " LFIRST(1)=.TRUE."
	print >> cont, " NMODLS(1)=2"
	print >> cont, " CMIXLA(1)="+str(CMIXLA)+"D0"
	print >> cont, " RSCLX(1)="+str(X)+"D0"
	print >> cont, " RSCLZ(1)="+str(Z)+"D0"
	print >> cont, ""
	print >> cont, " KINDRN(2)=1"
	print >> cont, " LFIRST(2)=.FALSE."
	print >> cont, " NMODLS(2)= " + str(int(NMOD))
	print >> cont, " CMIXLA(2)="+str(float(CMIXLA))+"D0"
	print >> cont, " ENDAGE(2)="+str(endage)+"D9"
	print >> cont, ""
	print >> cont, " LOPAL95=.TRUE."
	print >> cont, " FO95COBIN='"+ head +"/opac/OPAL/OPAL_GS98.bin'"
	print >> cont, ""
	print >> cont, " LALEX95=.TRUE."
	print >> cont, " ZALEX="+str(Z)+"D0"
	print >> cont, ""
	print >> cont, " MIX='GS98'"
	print >> cont, " IAFE=0"
	if asteroseismic:
		print >> cont, ""
		print >> cont, " LPULSE=.TRUE."
	print >> cont, ""
	print >> cont, " LZAMS=.FALSE."
	print >> cont, " LHB=.FALSE."
	print >> cont, " LTRACK=.TRUE."
	print >> cont, " LISO=.TRUE."
	print >> cont, " LCORR=.TRUE."
	print >> cont, " LRWSH=.FALSE."
	print >> cont, ""
	print >> cont, " OPECALEX(1)='"+ head +"/opac/ferg04/gs98.0.tron'"
	print >> cont, " OPECALEX(2)='"+ head +"/opac/ferg04/gs98.1.tron'"
	print >> cont, " OPECALEX(3)='"+ head +"/opac/ferg04/gs98.2.tron'"
	print >> cont, " OPECALEX(4)='"+ head +"/opac/ferg04/gs98.35.tron'"
	print >> cont, " OPECALEX(5)='"+ head +"/opac/ferg04/gs98.5.tron'"
	print >> cont, " OPECALEX(6)='"+ head +"/opac/ferg04/gs98.7.tron'"
	print >> cont, " OPECALEX(7)='"+ head +"/opac/ferg04/gs98.8.tron'"
	print >> cont, " OPECALEX(8)='"+ head +"/opac/ferg04/gs98.9.tron'"
	print >> cont, ""
	print >> cont, " $END"

	cont.close()
	return 0

	cont.close()
	return 0



def update_phys(phys_file_name,atm,eta_D,ovs, FREEOS, *args, **kwargs):
	asteroseismic=bool(kwargs.get('asteroseismic',False))
	phys=open(phys_file_name,"w")	 

	print >> phys, "$PHYSICS"
	print >> phys, " KTTAU=" +str(int(atm))
	print >> phys, ""
	print >> phys, " LDIFY = .TRUE."
	print >> phys, " LDIFZ=.TRUE."
	print >> phys, " LTHOUL=.TRUE."
	print >> phys, " LTHOULFIT = .FALSE."
	print >> phys, " FGRY = " +str(eta_D)+"D0"
	print >> phys, " FGRZ = "+str(eta_D)+"D0"
	print >> phys, " DT_GS = 0.1D0         "
	print >> phys, " XMIN = 1.0D-3         "
	print >> phys, " YMIN = 1.0D-3         "
	print >> phys, " GRTOL = 2.0D-7        "
	print >> phys, " NITER_GS = 10         "
	print >> phys, " ILAMBDA = 4"
	print >> phys, ""
	print >> phys, " LNEWS=.TRUE."
	print >> phys, " LSNU=.TRUE."
	print >> phys, ""	
	print >> phys, " NITER1=2"
	print >> phys, " NITER2=40"
	print >> phys, " NITER3=0"
	print >> phys, " NITER4=0"
	print >> phys, ""
	print >> phys, " LSEMIC=.FALSE.      "
	print >> phys, " DPENV=1.00"
	print >> phys, " LOVSTC=.TRUE.        "
	print >> phys, " ALPHAC=" + str(ovs)
	print >> phys, " LOVSTE=.TRUE.        "
	print >> phys, " LOVSTM=.FALSE.         "
	print >> phys, ""
	print >> phys, " LEXCOM=.FALSE.         "
	print >> phys, ""	
	print >> phys, " LENVG=.TRUE.         "
	print >> phys, " ATMSTP=0.0050           "
	print >> phys, " ENVSTP=0.0050         "
	print >> phys, ""	
	print >> phys, " LCOREL=.TRUE."
	print >> phys, " LHAFT=.TRUE."
	print >> phys, " LNULOS1=.TRUE."
	print >> phys, "  LNULOS2=.TRUE."
	print >> phys, ""
	print >> phys, "  LROT=.FALSE."
	print >> phys, ""	
	print >> phys, "  LFREE_EOS=."+str(FREEOS)+ "."
	print >> phys, "  IEOS=1,101,0"
	print >> phys, "  LOPALE=.FALSE."
	print >> phys, "  LDH=.TRUE.         "
	print >> phys, "  ETADH0 = -1.0D0"
	print >> phys, "  ETADH1 = 1.0D0	 "
	print >> phys, ""
	print >> phys, "  LCORE=.FALSE.                                "
	print >> phys, "  FCORE=1.0"
	print >> phys, "  MCORE=1              	 "
	print >> phys, ""
	print >> phys, "  LNEWCP=.FALSE.        "
	print >> phys, "  ANEWCP='   '          "
	print >> phys, "  ATMP='REL'            "
	print >> phys, "  XNEWCP=13              "
	print >> phys, ""	
	print >> phys, "  FCORR0=0.8D0            "
	print >> phys, "  FCORRI=0.1D0      "
	print >> phys, ""
	print >> phys, "  LNEW0=.FALSE."
	print >> phys, "  TRIDT=1.0D-3"
	print >> phys, "  TRIDL=8.0D-3          "
	print >> phys, "  "
	print >> phys, " ATMERR=1.0D-5 "
	print >> phys, "  ATMMAX=0.05D0         "
	print >> phys, "  ATMMIN=0.015D0           "
	print >> phys, "  ATMBEG=0.015D0"
	print >> phys, "  ATMD0=1.0D-10         "
	print >> phys, "  ENVERR=1.0D-5        "
	print >> phys, "  ENVMAX=0.05D0         "
	print >> phys, "  ENVMIN=0.015D0           "
	print >> phys, "  ENVBEG=0.015D0            "
	print >> phys, "  STOLR0=1.0D-7         "
	print >> phys, "  IMAX=11               "
	print >> phys, "  NUSE=7      "
	print >> phys, " 	 "

	if asteroseismic:
		print(r"\n\nWARNING! Asteroseismic tolerances in use!!!!\n\n")
		print >> phys, "  HTOLER(1,1)=6.0D-6"
		print >> phys, "  HTOLER(2,1)=4.5D-6    "
		print >> phys, "  HTOLER(3,1)=3.0D-6    "
		print >> phys, "  HTOLER(4,1)=9.0D-6    "
		print >> phys, "  HTOLER(5,1)=3.0D-6    "
	else:
		print("---------------------------- STANDARD TOLERANCES IN USE ----------------------------")
        print >> phys, "  HTOLER(1,1)=6.0D-5"
        print >> phys, "  HTOLER(2,1)=4.5D-5    "
        print >> phys, "  HTOLER(3,1)=3.0D-5    "
        print >> phys, "  HTOLER(4,1)=9.0D-5    "
        print >> phys, "  HTOLER(5,1)=3.0D-5    "


	print >> phys, "  HTOLER(1,2)=9.0D4"
	print >> phys, "  HTOLER(2,2)=5.0D4    "
	print >> phys, "  HTOLER(3,2)=5.0D4    "
	print >> phys, "  HTOLER(4,2)=5.0D10"
	print >> phys, "  HTOLER(5,2)=2.5D-6"
	print >> phys, "  "
	print >> phys, "  SHELLTOL(1)=1.0D-10"
	print >> phys, "  SHELLTOL(2)=1.0D-2"
	print >> phys, "  SHELLTOL(3)=5.0D-2"
	print >> phys, "  SHELLTOL(4)=1.0D0         "
	print >> phys, "  SHELLTOL(5)=1.0D0       "
	print >> phys, "  SHELLTOL(6)=1.0D0     "
	print >> phys, "  SHELLTOL(7)=0.0D0"
	print >> phys, " "
	print >> phys, "  SHELLTOL(8)=1.0D-2        "
	print >> phys, "  SHELLTOL(9)=1.0D-2      "
	print >> phys, "  SHELLTOL(10)=1.0D-2"
	print >> phys, "  SHELLTOL(11)=1.0D-2  "
	print >> phys, "  "
	print >> phys, "  SHELLTOL(12)=0.1D0"
	print >> phys, " "
	print >> phys, "  ATIME(1)=1.0D-4"
	print >> phys, "  ATIME(2)=1.0D-3       "
	print >> phys, "  ATIME(3)=3.0D-2        "
	print >> phys, "  ATIME(4)=2.0D-2"
	print >> phys, "  ATIME(5)=3.0D-2      "
	print >> phys, "  ATIME(6)=1.5D-3"
	print >> phys, "  ATIME(7)=1.0D-1      "
	print >> phys, "  ATIME(8)=2.0D-2"
	print >> phys, "  ATIME(9)=2.0D-2     "
	print >> phys, "  ATIME(10)=2.0D-2      "
	print >> phys, "  ATIME(11)=2.0D-2"
	print >> phys, "  ATIME(13)=1.05d0"
	print >> phys, "  LPTIME=.TRUE.        "
	print >> phys, " 	 "
	print >> phys, "  TCUT(1)=6.5D0           "
	print >> phys, "  TCUT(2)=6.5D0          "
	print >> phys, "  TCUT(3)=6.82D0          "
	print >> phys, "  TCUT(4)=7.73D0          "
	print >> phys, "  TCUT(5)=7.5D0           "
	print >> phys, "  TSCUT=6.0D0             "
	print >> phys, "  TENV0=3.0D0             "
	print >> phys, "  TENV1=9.0D0             "
	print >> phys, "  TGCUT=6.9D0             "
	print >> phys, "                        "
	print >> phys, "  OPTOL=1.0D-8"
	print >> phys, "  CMIN = 1.0D-20"
	print >> phys, "  ABSTOL = 1.0D-6"
	print >> phys, "  RELTOL = 1.0D-5"
	print >> phys, "  KEMMAX = 50"
	print >> phys, " "
	print >> phys, "  CLSUN = 3.828D33"
	print >> phys, "  CRSUN=6.957D10"
	print >> phys, " "
	print >> phys, "  SStandard=0.997543,1.02913,1.03704,0.965517,1.47273,0.478916,1.12766,1.0,1.0/"
	print >> phys, "  ,1.0,1.0,1.0,1.0,1.0,1.01083,0.876543,1.075,0.625,1.21795"
	print >> phys, " "
	print >> phys, " $END"

	phys.close()

	return 

def update_shell(run_file,prems_model_dir,input_model,phys_file_name,cont_file_name, *arg, **kwargs):
	#run_file, input_model, output_iso_name, prems_dir
	which_comp=str(kwargs.get('which_comp',''))
	head = str(kwargs.get('head', ''))
	output_dir=str(kwargs.get('output_dir',''))

	#print "(loc 2 ) prems_model_dir: ", prems_model_dir

	asteroseismic=bool(kwargs.get('asteroseismic',False))

	if which_comp!='Erika':
		comp_str='meridith'
	else:
		comp_str='mjoyce'

	phys_file_piece=str(phys_file_name).split('.nml')[0].split('/nml/')[1]
	cont_file_piece=str(cont_file_name).split('.nml')[0].split('/nml/')[1]

	run=open(run_file,"w")

	print >> run, "# ! /bin/bash"
	print >> run, "#  this file executes dsep3"

	### special cases for badly configured computers:
	if which_comp == 'LMC':
		print >> run, "LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/free_eos-2.2.1/install_dir/lib"
	elif which_comp== 'Marsha':
		print >> run, "#"

	elif which_comp=="Erika":
		print >> run, "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/meridith/free_eos-2.2.1/lib"
		print >> run, "LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/free_eos-2.2.1/lib"
		print >> run, "ldd /home/meridith/dsep3/dsepX/dsepX"

	### everything else
	else:
		print >> run, "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:"+head.split('/dsep3')[0]+"free_eos-2.2.1/lib"
		print >> run, "LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/free_eos-2.2.1/lib"
		print >> run, "ldd "+head+"dsepX/dsepX"
	

	print >> run, ""
	print >> run, "local=$HOME/dsep3"
	print >> run, "nml=$local/nml"
	print >> run, "out=$local/out"
	print >> run, "prog=$local/dsepX"
	print >> run, "zams=$local/zams"
	print >> run, "prems=$local/prems"
	print >> run, "opac=$local/opac"
	print >> run, "atm=$local/surfBC"
	print >> run, "opal=$opac/OPAL"
	print >> run, "phx=$opac/phoenix"
	print >> run, "bcphx=$atm/phoenix/GS98"
	print >> run, "bckur=$atm/atmk"
	print >> run, "out_meridith=$local/run/out_meridith/"+output_dir
	print >> run, ""
	print >> run, "outname="+str(input_model)
	print >> run, ""
	print >> run, "rm fort.*"
	print >> run, " ln  -s $nml/"+str(phys_file_piece)+".nml			fort.13"
	print >> run, " ln  -s $nml/"+str(cont_file_piece)+".nml                    fort.14"
	print >> run,""
	print >> run, "# input opacities/boundry conditions; Fergson low T specified in CONTROL nml"
	print >> run, " ln  -s $opac/FERMI.TAB                  fort.15"
	print >> run, " ln  -s $bckur/atmk1990p00.tab           fort.38"
	print >> run, " ln  -s $opal/GS98hz                     fort.48"
	print >> run, "# Phoenix boundary conditions, code picks correct Z, multipe ones "
	print >> run, "# to allow for correct BC when rescaling"
	print >> run, " ln  -s $bcphx/z_p0d0.afe_p0d0.dat       fort.95"
	print >> run, " ln  -s $bcphx/z_m0d5.afe_p0d0.dat       fort.96"
	print >> run, " ln  -s $bcphx/z_m0d7.afe_p0d0.dat       fort.97"
	print >> run, " ln  -s $bcphx/z_m1d0.afe_p0d0.dat       fort.98"
	print >> run, " ln  -s $bcphx/z_m1d5.afe_p0d0.dat       fort.99"
	print >> run, ""
	print >> run, "# input model"
	print >> run, " ln  -s $prems/"+str(prems_model_dir)+"/"+str(input_model)+" 				fort.12"
	print >> run, ""
	print >> run, "# output"
	print >> run, " ln  -s $out_meridith/$outname.track         fort.19"
	print >> run, " ln  -s $out/$outname.short                  fort.20"
	print >> run, " ln  -s $out_meridith/$outname.iso			fort.37" 
	print >> run, " ln  -s $out_meridith/$outname.last          fort.11"
	print >> run, ""
	if asteroseismic:
		print >> run, "ln -s $out_meridith/$outname.fpmod					fort.24"
		print >> run, "ln -s $out_meridith/$outname.fpenv					fort.25"
		print >> run, "ln -s $out_meridith/$outname.fpatm					fort.26"
		print >> run, ""
	print >> run, "time $prog/dsepX"

	run.close()

	#subprocess.call('chmod +x '+run_file,shell=True)

	return 


def make_prems_models(mstar,amlt,zin,yin, *args, **kwargs):
	###### THIS DOES NOT CARE ABOUT OVERSHOOT, MIXING EFFICIENCY, ATMOSPHERE, ETC
	###### THIS IS JUST A PILE OF GAS
	###### THIS ONLY CARES ABOUT COMPOSITION
	which_comp=str(kwargs.get('which_comp',''))
	head     = str(kwargs.get('head', ''))
	if which_comp=='Erika':
		mname='meridith'
	else:
		mname='mjoyce'

	#config=int(kwargs.get('config',True))
	model_ID_head = str(kwargs.get('model_ID_head', ''))
	model_dir= str(kwargs.get('model_dir', ''))

	print "(loc 6) model_dir:", model_dir

	aFe=float(kwargs.get('aFe',0.0))


	starting_mass=int(float(mstar)*1000.)
	interval=5#100
	ending_mass=int(float(mstar)*1000.) + interval 

	print_zin=('%1.3f'%float(zin))
	print_yin=('%1.2f'%float(yin))
	print_mlt=('%1.3f'%float(amlt))

	model_ID=str(kwargs.get('model_ID',model_ID_head+"."+print_mlt+'.Z'+print_zin+'.Y'+print_yin))
	print "loc 10 model_ID", model_ID

	GP.make_prems_model(amlt, zin, yin, aFe, starting_mass, ending_mass, model_dir, interval, model_ID,\
		which_comp=which_comp, head=head)
	return 



def make_solar_prems_model(tag, amlt, zin, yin, *args, **kwargs):
	###### THIS DOES NOT CARE ABOUT OVERSHOOT, MIXING EFFICIENCY, ATMOSPHERE, ETC
	###### THIS IS JUST A PILE OF GAS
	###### THIS ONLY CARES ABOUT COMPOSITION
	which_comp=str(kwargs.get('which_comp',''))
	if which_comp=='LMC':
		mname='mjoyce'
	else:
		mname='meridith'

	mstar=1.0
	aFe=0.0
	model_dir= str(kwargs.get('model_dir', 'solar_calibrations'))
	model_ID=tag+'.solar.MIX_'+ ('%1.5f'%amlt)+'.Y_'+('%1.3f'%yin) +'.Z_'+('%1.4f'%zin)
	make_prems_models(mstar,amlt,zin,yin,model_ID=model_ID,model_dir=model_dir, which_comp=which_comp, path=head)
	return 


def do_run(mstar,amlt,zin,yin, shell_file, cont_file,phys_file,\
	 run_dir, atm, eta_D,ovs, FREEOS, *args, **kwargs):

	###################
	#
	# kwargs
	#
	###################
	which_comp=str(kwargs.get('which_comp',''))
	NMOD=int(kwargs.get('NMOD',9999))
	endage=float(kwargs.get('endage',-4.7))
	model_ID_head = str(kwargs.get('model_ID_head', ''))
	prems_model_dir= str(kwargs.get('prems_model_dir', ''))
	head = str(kwargs.get('head', ''))

	#print "(loc 3 )prems_model_dir: ", prems_model_dir

	output_dir =str(kwargs.get('output_dir', ''))
	asteroseismic=bool(kwargs.get('asteroseismic',False))


	print "using:\n", cont_file, "\n", shell_file, "\n"
	#print "value of run_dir: ", run_dir
	#run=shell_file.split('/dsep3/')[1] #+run_dir+'/')
	#run=run_dir

	mstar=100.*float(mstar)
	mstar=('%1.1f'%mstar)
	print_zin=('%1.3f'%float(zin))
	print_yin=('%1.2f'%float(yin))
	print_mlt=('%1.3f'%float(amlt))
	model_ID=str(kwargs.get('model_ID',model_ID_head+"."+print_mlt+'.Z'+print_zin+'.Y'+print_yin))
	if float(mstar) < 100.0:
		out_iso_name ="m0"+str(mstar)+"."+model_ID
	else:
		out_iso_name = "m"+str(mstar)+"."+model_ID 


	update_phys(phys_file ,atm, eta_D, ovs, FREEOS)
	update_cont(cont_file, amlt, zin, yin, NMOD,\
		endage=endage, which_comp=which_comp,asteroseismic=asteroseismic, head=head) 
	print "shell_file before update shell ", shell_file


	update_shell(shell_file,prems_model_dir,out_iso_name,phys_file, cont_file,\
	 	which_comp=which_comp,output_dir=output_dir,asteroseismic=asteroseismic, head=head)
	

	print "(loc 4 )prems_model_dir: ", prems_model_dir


	os.chdir('../'+run_dir+'/')

	print "shell file: ", shell_file, "  run_dir", run_dir
	run_piece=shell_file.split(run_dir+'/')[1] #.split('/')[-1] + '.sh'
	# print "run_piece", run_piece

	subprocess.call("chmod +x "+shell_file, shell=True)
	subprocess.call("./"+run_piece, shell=True)

	print r"\n\do_run terminated successfully"
	return 


def make_input_prems_sets(mhead,mixing_lengths,yins,zins,*args, **kwargs):
	which_comp=str(kwargs.get('which_comp',''))
	if which_comp=='LMC':
		mname='mjoyce'
	else:
		mname='meridith'

	CMIXLA_list=np.array(mixing_lengths)
	Zsolar_list=np.array(zins)
	helium_list=np.array(yins)

	for k in range(len(Zsolar_list)):
		Zsolar=Zsolar_list[k]
		for i in range(len(CMIXLA_list)):
			CMIXLA=CMIXLA_list[i]
			for j in range(len(helium_list)):
				He=helium_list[j]
				make_solar_prems_model(mhead,CMIXLA,Zsolar,He, model_dir='solar_calibrations',which_comp=which_comp)

	return 


def solar_calibrate(mhead,run_dir,mixing_lengths,yins,zins, atm, eta_D, ovs,*args,**kwargs):
	which_comp=str(kwargs.get('which_comp',''))
	if which_comp!='Erika':
		mname='mjoyce'
	else:
		mname='meridith'

	mstar=1.0
	FREEOS="FALSE"
	endage=4.603

	try:
		run_dir_piece=run_dir.split('/home/'+mname+'/dsep3/')[1].split('/')[0]
	except IndexError:
		run_dir_piece=run_dir

	cont_file='/home/'+mname+'/dsep3/nml/cont_solar_'+run_dir_piece+'.nml'
	shell_file='/home/'+mname+'/dsep3/'+run_dir+'/run_solar_'+run_dir_piece+'.sh'
	phys_file='/home/'+mname+'/dsep3/nml/phys_solar_'+run_dir_piece+'.nml'

	CMIXLA_list=np.array(mixing_lengths)
	Zsolar_list=np.array(zins)
	helium_list=np.array(yins)

	for k in range(len(Zsolar_list)):
		Zsolar=Zsolar_list[k]
		for i in range(len(CMIXLA_list)):
			CMIXLA=CMIXLA_list[i]
			for j in range(len(helium_list)):
				He=helium_list[j]
				model_ID=mhead+'.solar.MIX_'+ ('%1.5f'%CMIXLA)+'.Y_'+('%1.3f'%He) +'.Z_'+('%1.4f'%Zsolar)
				do_run(mstar,CMIXLA,Zsolar,He, shell_file, cont_file,phys_file, run_dir,atm, eta_D,ovs, FREEOS,\
				endage=endage, prems_model_dir='solar_calibrations',output_dir='solarCalibrate',model_ID=model_ID, which_comp=which_comp)
	return 0


def set_par(tag):
	tag = str(tag)
	if tag =='ttau':
		atm,eta_D,ovs=0,1.0,0
	elif tag =='ks':
		atm,eta_D,ovs=1.0,1.0,0
	elif tag =='0p5':
		atm,eta_D,ovs=0.0,0.5,0
	elif tag =='1p5':
		atm,eta_D,ovs=0.0,1.5,0
	elif tag =='1p5ovs':
		atm,eta_D,ovs=0.0,1.5,0.1
	else:
		print "tag type unknown!"
		sys.exit()

	return atm,eta_D,ovs
