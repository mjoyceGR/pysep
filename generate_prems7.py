#!/usr/bin/env python 
import subprocess
import numpy as np
import shutil
import os
import sys
import glob


###### THIS DOES NOT CARE ABOUT OVERSHOOT, MIXING EFFICIENCY, ATMOSPHERE, ETC
###### THIS IS JUST A PILE OF GAS
###### THIS ONLY CARES ABOUT COMPOSITION

def make_prems_model(mixing_length, Z, Y, aFe, starting_mass, ending_mass,\
  					model_dir,interval,model_ID, *args,**kwargs):

	head = str(kwargs.get('head', ''))
	#print "head: ", head
	# sys.exit()

	which_comp=str(kwargs.get('which_comp',''))
	if which_comp!='Erika':
		mname='mjoyce'
	else:
		mname='meridith'
	#print "COMPUTER BEING USED IS", which_comp
	
	CMIXLA=mixing_length #1.94465
	low_mass=starting_mass#990#700 
	high_mass=ending_mass #1010#950 
	interval = interval

	Y_BBN=0.245
	Y_solar=0.28
	Z_solar=0.019

	Zabund=Z
	#default_Yabund = float(Y_BBN) + ( (float(Y_solar) - float(Y_BBN))/float(Z_solar) ) * float(Zabund)
	Yabund=Y

	#print "Yabund: ", Yabund 
	Xabund=1.0-Yabund-Zabund
	RSCLX=Xabund 

	ID = str(model_ID)# +str(CMIXLA) #FREEOS.ML_
			#	0      1      2	        3	 4 	  5 6         7 8 	
	elem_t=(1.0e22,3.0e-5,2.8995e-3,2.865e-5,8.493e-4,0,7.8858e-3,0,0) #elem_00
	elem04=(1.0e22,3.0e-5,2.850e-3,2.865e-5,8.350e-4,0,1.9470e-2,0,0)

	#input parameters (constant), to be printed to the nml file
	z_solar   = Z_solar
	delta     = 1.0
	delta0    = 0
	beta      = 1.000
	cmixl     = CMIXLA
	ddage     = 1000.0
	fmass1    = 0.0000099
	fmass2    = 0.9999
	pn        = 1.5
	lexcom    = '.FALSE.'

	if aFe == 0.0: ## elem*, WHICHEVER, gets adjusted according to METALLICTY whether it's the alpha enhanced one or NOT
		elem=elem_t
	else:
		elem=elem04
	#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	## is this array the same as the hard-coded elem04 one above??
	#print "aFe: ", aFe, " which elem?: ", elem

	make_elem=[]
	for q in range(len(elem)):
		make_elem.append(elem[q] * (Zabund/Z_solar))
	#make_elem=np.array(make_elem)
	make_elem[0]=1.0e22
	make_elem[1]=3.0e-5
	elem=make_elem
	
	locdir    = head #"/home/"+mname+"/dsep3"
	poly      = locdir+"/poly"
	prems     = locdir+"/prems/"+model_dir

	#print "locdor, model_dir:", locdir, model_dir
	#sys.exit()

	Ladjust=-0.115*np.log(float(Zabund)/float(z_solar))/np.log(10.)
	Tadjust=-0.022*np.log(float(Zabund)/float(z_solar))/np.log(10.)

	
	## INSERT ADDITIONAL CONDITIONS ON L, Teff HERE 8/23/17
	for i in range(low_mass,high_mass,interval):########## 1 corresponds to 0.1 because we're diving by 1000
	 	m=i/1000. 
	 	if(m<=3.0):
	 		teff=0.039*m + 3.5765
	 	if(m<=1.5):
			lum =0.85*m + 0.4
		if(m>1.5):
			lum=1.7
	    
	    	if(m>3.0):
	      		teff=-0.028*m + 3.785
	      		lum =0.55*m+0.1

		if(m>5.0):
	      		teff=3.64 
	      		lum=2.6+0.2*(m-5.0) 
	      
	     	teff= teff +  Tadjust 
	     	lum = lum  +  Ladjust 

		
		## with starting_mass and ending_mass defined to be length 1, this should never run more than once
		model = print_polynml(poly, i, ID, prems,\
		 			  m, teff, lum, RSCLX, Zabund,\
		 			  elem, cmixl, beta, fmass1, fmass2, ddage, pn, lexcom)

	# print "\ngenerate_prems.py for "+model+" executed successfully\n\n"  
	#print "model name: ", model
	return model




def print_polynml(poly, i, ID, prems, \
				  m, teff, lum, RSCLX, Zabund,\
 				  elem, cmixl, beta, fmass1,\
 				  fmass2, ddage, pn,lexcom):
	
	POLY=open(poly+"/poly.nml","w") 
	#print "got here (loc 15)"
	print >> POLY, " $DATA\n SUMASS =",('%6.3f' % m),"\n TEFFL1 =",('%5.2f' % teff)#,"\n"#,  m,  teff 
	print >> POLY, " SULUML =",('%5.2f' % lum)#,"\n"#,  lum 
	print >> POLY, " X =",RSCLX,"\n Z =",Zabund #,"\n" #changed form "x" to "RSCLX"

	for j in range(len(elem)):
		z_elem =  Zabund*elem[j]
		if j!=0: 
			print >>  POLY, " ELEM("+str(j)+") = "+str(elem[j])

	print >> POLY, " CMIXL = ",cmixl,"\n BETA = ",beta,"\n FMASS1 = ",fmass1
	print >> POLY, " FMASS2 =", fmass2,"\n DDAGE = ",ddage,"\n PN = ",pn
	print >> POLY, " LEXCOM = ",lexcom
	print >> POLY, " $END" 
	POLY.close() 

	if(i<10000): #added zero
		istring=str(i)
		model = "m0" +istring[:2]+"."+istring[2:]+"."+ ID 
		if i >= 1000:
			model= "m" + istring[:3] + "." +istring[3:] + "." + ID
	else:
		print "invalid model name construction, mass parsed as",i/1000
		sys.exit()


	existing_files=glob.glob(prems+"/*")
	#print existing_files
	#print "model", model
	#sys.exit()

	if (prems+str(model)) in existing_files:
		print "pre-ms model with this name alreayd exists, skipping..."
		#import time
		#time.sleep(1)
	else:
		os.chdir(poly)
		subprocess.call("rm fort.*", shell=True)
		subprocess.call("./testpoly", shell=True)
		#os.listdir(poly)

		just_made = prems+"/"+model
		shutil.move("fort.12",just_made) 
		print "\ngenerate_prems.py for "+model+" executed successfully\n\n"  
	## not sure what's going on here
	# if( i>=10): 
	# 	delta=0.1 #0.1 # WAS 5 CHANGED TO 1 temporarily #changes the step size which is why first variable doesn't work
	# if( i>=180):
	# 	delta=10
 #    	if( i>=300):
	# 	delta=20
	return model 