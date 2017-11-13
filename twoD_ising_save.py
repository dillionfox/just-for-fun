from __future__ import division	# in case I divide two integers 
import numpy as np
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
import math, random
import time, datetime

### user parameters ###
Nx = 10									# number of points in x-direction
Ny = 10									# number of points in y-direction
numsteps = 100 							# number of MC steps in equilibration stage
data_steps = 100							# number of additional MC steps for data collection

dT = 2.0								# step size
Tstart = 1								# lowest temperature to consider
Tstop = 5.1								# highest temperature to consider

dH = 1.0								# step size
Hstart = -5.0								# lowest temperature to consider
Hstop = 5.1								# highest temperature to consider

numTpoints = math.ceil((Tstop-Tstart)*(1/dT))				# how many temperatures will be run total
numHpoints = math.ceil((Hstop-Hstart)*(1/dH))				# how many temperatures will be run total
T_list = np.linspace(Tstart, Tstop, numTpoints)				# array containing all T values
H_list = np.linspace(Hstart, Hstop, numHpoints)				# array containing all T values
E_list = np.zeros((numTpoints,numHpoints))				# empty array that will contain all E values for each value of T
M_list = np.zeros((numTpoints,numHpoints))				# empty array that will contain all M  values for each value of T 
B_list = np.zeros((numTpoints,numHpoints))				# empty array that will contain all beta*mu*H  values for each value of T 

### visualize results ###
def make_plots(Energy,Magnetization,T,Beta_mu_B):
	global Nx, Ny
	
	f=plt.figure(figsize=(18, 10),dpi=80);    

	colors=['b','g','r','c','m','y','k']
	yaxisname="Magnetization"
	xaxisname="H"
	fig=f.add_subplot(3,1,1);	
	for i in range(Magnetization.shape[1]):
		plt.plot(Beta_mu_B[:,i],Magnetization[:,i],color=colors[i%7]);
		plt.scatter(Beta_mu_B[:,i],Magnetization[:,i],color=colors[i%7]);
	plt.xlabel(xaxisname,fontsize=20);
	plt.ylabel(yaxisname,fontsize=20);
	#return Beta_mu_B, Magnetization
	savedata(Beta_mu_B,Magnetization,yaxisname,xaxisname,Nx,Ny)
	
	fig=f.add_subplot(3,1,2);
	yaxisname2="Magnetization"
	xaxisname2="Temperature"
	plt.scatter(T,abs(Magnetization[:,0]),color='r',label='Magnetization');
	plt.plot(T,abs(Magnetization[:,0]),label='Magnetization');
	plt.ylabel(yaxisname2,fontsize=20);
	plt.xlabel(xaxisname2,fontsize=20);
	savedata(T,abs(Magnetization[:,0]),yaxisname2,xaxisname2,Nx,Ny)

	fig=f.add_subplot(3,1,3);	
	yaxisname3="Energy"
	xaxisname3="Temperature"
	plt.scatter(T,Energy, color='r',label=' Energy');
	plt.plot(T,Energy,label=' Energy');
	plt.ylabel(yaxisname3,fontsize=20);
	plt.xlabel(xaxisname3,fontsize=20);
	savedata(T,Energy,yaxisname3,xaxisname3,Nx,Ny)
	
	plt.show()
	#filename="1D_E-vs-T_M-vs-T.png"
	#plt.savefig(filename)

def savedata(a,b,yname,xname,nx,ny):
	
	### output name ###
	t = time.time()
	date = datetime.datetime.fromtimestamp(t).strftime('%m-%d_%H_%M_%S')	#to keep track of when I ran this and to avoid overwritting previous saved files
	name=str(date)
	outfile=open(yname+"-vs-"+xname+"_("+str(nx)+"x"+str(ny)+")_"+name+".csv", "w+")
	
	#assuming arrays a and b are of the same dimensions as one would expect for a list of (x,y) points
	L = len(a)
	
	#stupid, I know, but, it works
	if (xname=="Temperature"):
		for i in range(L):
			line = "%s,%s\n" %(str(a[i]),str(b[i]))
			outfile.write(line)
		outfile.closed
	else:	
		for i in range(L):
			for j in range(len(a[i])):
				line = "%s,%s\n" %(str(a[i][j]),str(b[i][j]))
				outfile.write(line)
			outfile.write("\n")
		outfile.closed

### initialize ###
def initialize():
	s=np.ones((Nx,Ny),int)						# generate Nx x Ny matrix full of +/-1
	for i in range(Nx):
		for j in range(Ny):
			s[i,j]=1 if random.random()<0.5 else -1
	return s

### monte carlo ###
def metropolis(s, T, H):
	for nx in range(Nx):						# limits on sums are arbitrary, but they seem good enough
		for ny in range(Ny):					# just big enough for the system to equilibrate
			i=np.random.randint(0, Nx)			# randomly choose x
			j=np.random.randint(0, Ny)			# randomly choose y
			barrier=2*s[i,j]*(s[(i+1)%Nx,j]+s[i,(j+1)%Ny]+s[(i-1)%Nx,j]+s[i,(j-1)%Ny])+H*s[i,j]
			if barrier<0 or random.random()<math.exp(-barrier/T):
				s[i,j]=-s[i,j]
	return s

### caluclate total energy ###
def totalEnergy(s,H):
	energy=0
	for i in range(len(s)):						# iterate through all elements of s and compute total energy
		for j in range(len(s)):
			energy += -s[i,j]*(s[(i+1)%Nx,j]+s[i,(j+1)%Ny]+s[(i-1)%Nx,j]+s[i,(j-1)%Ny])-H*s[i,j]
	return energy

### main procedure ###
def main():
	for T in range(len(T_list)):					# loop over all temperatures between Tstart and Tstop in steps of dT
		for H in range(len(H_list)):				# loop over all temperatures between Tstart and Tstop in steps of dT
			s=initialize()					# initialize Nx x Ny matrix with random +/-1
			E_ave=0
			M_ave=0
			for i in range(numsteps): 			# run for a while
				s=metropolis(s,T_list[T],H_list[H])	# execute Nx*Ny MC steps, then report back with updated matrix
			for j in range(data_steps):			# average over data points at the end
				s=metropolis(s,T_list[T],H_list[H])	# run for additional steps in equilibrated state to collect data
				E_ave+=totalEnergy(s,H_list[H])/(data_steps*Nx*Ny)
				M_val = np.sum(s)/(data_steps*Nx*Ny)
				M_ave+=M_val
			#outfile.write("%s,%s,%s\n" %(str(T),str(H),str(M_val)))
			E_list[T,H]=E_ave
			M_list[T,H]=M_ave				# magnitude of M
			B_list[T,H]=float(H_list[H]/T_list[T])
	make_plots(E_list[:,0],M_list,T_list,B_list)
	#return b,m

main()									# initiate 

