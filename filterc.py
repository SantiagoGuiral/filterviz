import numpy as np 

def clip(x_in,fs,ftype,fc1,fc2=1):

	fc1=float(fc1)
	if(ftype=="Lowpass" or ftype=="Highpass"):
		fc2=1
	else:
		fc2=float(fc2)

	#design of the filter
	fbins=2**int(np.ceil(np.log2(len(x_in)))) #M
	u=fbins/fs
	k1=int(fc1*u)
	k2=int(fc2*u)
	H=np.zeros(fbins,dtype=np.complex_)
    
	if ftype=="Lowpass":
		H[0:k1]=np.ones(k1,dtype=np.complex_)
		H[-k1:]=np.ones(k1,dtype=np.complex_)
	elif ftype=="Highpass":
		H[k1:-k1]=np.ones(fbins-2*k1,dtype=np.complex_)
	elif ftype=="Bandpass":
		Bw=abs(k2-k1)
		H[k1:k2]=np.ones(Bw,dtype=np.complex_)
		H[-k2:-k1]=np.ones(Bw,dtype=np.complex_)
	elif ftype=="Bandstop":
		H[0:k1]=np.ones(k1,dtype=np.complex_)
		H[k2:-k2]=np.ones(fbins-2*k2,dtype=np.complex_)
		H[-k1:]=np.ones(k1,dtype=np.complex_)
	else:
		print("KeyError: ftype not recognised on frecprodfilter.")
		return 1

	#fourier transform of the signal
	X=np.fft.fft(x_in,fbins)
	#filter product with the signal
	Y=H*X
    #time/sampling-domain signal
	y=np.fft.ifft(Y,fbins)[:len(x_in)]
	Hf=fourier.fftfreq(fbins,fs/fbins)

	return y,H,Hf

