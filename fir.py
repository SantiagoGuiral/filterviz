import numpy as np
import scipy.signal as signal
import math

def fir_windowing(fs,ftype,window,BW,ripple,fc1,fc2=1,Adb=0):

	#Normalize the frequencies
	wc1=(2*np.pi*fc1)/fs
	wc2=(2*np.pi*fc2)/fs
	bwn=(2*np.pi*BW)/fs

	#Ripple in dB
	rdb=20*np.log10(ripple)

	#Choose the order of the filter (M)
	if (rdb>=-13):            		#Rectangular
    	M=((4*np.pi)/bwn)-1
	elif (rdb>=-25):              	#Triangular
    	M=(8*np.pi)/bwn
	elif (rdb>=-31):  	            #Hann
    	M=(8*np.pi)/bwn
	elif (rdb>=-41):              	#Hamming
    	M=(8*np.pi)/bwn
	else:                         	#Blackman
	    M=(12*np.pi)/bwn

	M=math.ceil(M)
	if (M%2==0):
    	M+=1
    
	#Create the samples vector
	n=np.arange(int(-M/2),int(M/2+1))

	#Determines the Filter type 
	if (ftype=="Low"):
    	hx=(wc1/np.pi)*(np.sin(wc1*n)/wc1*n)
	    hx[int(M/2)]=(wc1/np.pi)
	elif (ftype=="High"):
	    hx=-(wc1/np.pi)*(np.sin(wc1*n)/wc1*n)
	    hx[int(M/2)]=1-(wc1/np.pi)
	elif (ftype=="Bandpass"):
	    hx=((wc2/np.pi)*np.sin(n*wc2))/(n*wc2)-((wc1/np.pi)*np.sin(n*wc1))/(n*wc1)
	    hx[int(M/2)]=(1/np.pi)*(wc2-wc1)
	elif (ftype=="Reject"):
	    hx=((wc1/np.pi)*np.sin(n*wc1))/(n*wc1)-((wc2/np.pi)*np.sin(n*wc2))/(n*wc2)
	    hx[int(M/2)]=1-((1/np.pi)*(wc2-wc1))

	#Determine the window
	if (window=="Default"):
		if (rdb>=-13):            		#Rectangular
			win=np.ones(len(hx))
		elif (rdb>=-25):              	#Triangular
			win=signal.triang(len(hx))
		elif (rdb>=-31):  	            #Hann
			win=signal.hann(len(hx))
		elif (rdb>=-41):              	#Hamming
			win=signal.hamming(len(hx))
		else:                         	#Blackman
	        win=signal.blackman(len(hx))
	elif (window=="Hamming"):
	    win=signal.hamming(len(hx))
	elif (window=="Hann"):
	    win=signal.hann(len(hx))
	elif (window=="Rectangular"):
	    win=np.ones(len(hx))
	elif (window=="Blackman"):
    	win=signal.blackman(len(hx))
	elif (window=="triangular"):
		win=signal.triang(len(hx))


	#Filter response
	hn=hx*win
	A=np.sqrt(10**(0.1*Adb))
	hn=hn*A

	return hn

