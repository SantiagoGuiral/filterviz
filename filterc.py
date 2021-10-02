import numpy as np 
from scipy.fft import fftfreq

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
	H=np.zeros(fbins,dtype=np.csingle)
    
	if ftype=="Lowpass":
		H[0:k1]=np.ones(k1,dtype=np.csingle)
		H[-k1:]=np.ones(k1,dtype=np.csingle)
	elif ftype=="Highpass":
		H[k1:-k1]=np.ones(fbins-2*k1,dtype=np.csingle)
	elif ftype=="Bandpass":
		Bw=abs(k2-k1)
		H[k1:k2]=np.ones(Bw,dtype=np.csingle)
		H[-k2:-k1]=np.ones(Bw,dtype=np.csingle)
	elif ftype=="Bandstop":
		H[0:k1]=np.ones(k1,dtype=np.csingle)
		H[k2:-k2]=np.ones(fbins-2*k2,dtype=np.csingle)
		H[-k1:]=np.ones(k1,dtype=np.csingle)
	else:
		print("KeyError: ftype not recognised on frecprodfilter.")
		return 1

	#fourier transform of the signal
	print(f'len x_in {len(x_in)}\t len fbin {fbins}')
	X=np.fft.fft(x_in,fbins)
	#filter product with the signal
	Y=H*X
    #time/sampling-domain signal
	y=np.fft.ifft(Y,fbins)[:len(x_in)]
	Hf=fftfreq(fbins,fs/fbins)

	return y,H,Hf

