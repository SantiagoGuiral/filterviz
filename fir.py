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
	if (ftype=="Lowpass"):
    	hx=(wc1/np.pi)*(np.sin(wc1*n)/wc1*n)
	    hx[int(M/2)]=(wc1/np.pi)
	elif (ftype=="Highpass"):
	    hx=-(wc1/np.pi)*(np.sin(wc1*n)/wc1*n)
	    hx[int(M/2)]=1-(wc1/np.pi)
	elif (ftype=="Bandpass"):
	    hx=((wc2/np.pi)*np.sin(n*wc2))/(n*wc2)-((wc1/np.pi)*np.sin(n*wc1))/(n*wc1)
	    hx[int(M/2)]=(1/np.pi)*(wc2-wc1)
	elif (ftype=="Bandstop"):
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
	elif (window=="Square"):
	    win=np.ones(len(hx))
	elif (window=="Blackman"):
    	win=signal.blackman(len(hx))
	elif (window=="Bartlett"):
		win=signal.triang(len(hx))


	#Filter response
	hn=hx*win
	A=np.sqrt(10**(0.1*Adb))
	hn=hn*A

	return hn

def freq_sampling(fs,ftype,N,fc1,fc2=1):
	#Limit for the IFT
	if (N%2!=0):
    	limit=(N-1)/2
	else:
    	limit=N/2 - 1

	limit=int(limit)

	#Sampling steps
	fk=fs/N
	samples=[i if N%2 else i+0.5 for i in range(limit+1)]
	hk=[]
	
	#Filter type
	if (ftype=="Low-pass"):
    for i in samples:
        if (fk*i<=fc1):
            hk.append(1)
        else:
            hk.append(0)
	elif(ftype=="High-pass"):
    	for i in samples:
        	if (fk*i<=fc1):
            	hk.append(0)
	        else:
    	        hk.append(1)
	elif(ftype=="Bandpass"):
    	for i in samples:
        	if (fk*i<=fc1 & fk*i>=fc2):
            	hk.append(0)
	        else:
    	        hk.append(1)       
	elif(ftype=="Bandstop"):
    	for i in samples:
        	if (fk*i>=fc1 & fk*i<=fc2):
            	hk.append(0)
	        else:
    	        hk.append(1)


	#Calculates the IFT
	alfa=(N-1)/2

	hn=np.zeros(limit+1)
	for n in range(limit+1):
    	acc=0
	    for k in range(1,limit+1):
	        acc+=2*hk[k]*np.cos((2*np.pi*k*(n-alfa))/N)
	    acc=(1/N)*(acc+hk[0])
	    hn[n]=acc
       
	#get the complete coeficients
	if (N%2!=0):
    	htemp=np.flip(hn[:-1])
	else:
    	htemp=np.flip(hn)
    
	h=np.concatenate((hn,htemp))


