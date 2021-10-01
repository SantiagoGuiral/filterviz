import numpy as np
import scipy.signal as signal
import math

def analog_irr (fs,N,ftype,fc1,fc2=1,att=3,ripple=5):

	#Normalize frequencies
	Td=1/fs
	
	waux1=2*np.pi*fc1
	waux2=2*np.pi*fc2
	
	wc1=(2/Td)*np.tan(waux1*Td/2)
	wc2=(2/Td)*np.tan(waux2*Td/2)

	#Choose filter band pass
	if(ftype=="Lowpass"):
	    wc=wc1
	    ftype="lowpass"
	elif(ftype=="Highpass"):
	    wc=wc1
	    ftype="highpass"
	elif(ftype=="Bandpass"):
	    wc=[wc1,wc2]
	    ftype="bandpass"
	elif(ftype=="Bandstop"):
	    wc=[wc1,wc2]
	    ftype="bandstop"

	#Determine the analog filter
	if(analog=="Butterworth"):
	    b,a=signal.butter(N, wc, ftype, analog='True')
	elif(analog=="Chebyshev I"):
	    b,a=signal.cheby1(N, ripple, wc, ftype, analog='True')
	elif(analog=="Chebyshev II"):
	    b,a=signal.cheby2(N, att, wc, ftype, analog='True')
	elif(analog=="Bessel"):
	    b,a=signal.bessel(N, wc, ftype, analog='True')
	elif(analog=="Elliptic"):
    	b,a=signal.ellip(N, ripple, att, wc, ftype, analog='True')
	
	#Bilinear Transform analog to digital filter
	z,p=signal.bilinear(b,a,fs=fs)

	return z,p
	
