import tkinter as tk
import sounddevice as sd
import soundfile as sf
import queue
import threading
import wave
import pygame
import math
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import filterc as fideal
import filterfir as ffir
import filteriir as fiir
from scipy.io.wavfile import read, write
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

def plot_time():

	if file_exists:
		file_audio=('./audios/recording.wav')
		fs,x=read(file_audio)
		x=x/float(np.max(np.abs(x)))
		x=x-np.mean(x)
		t=np.arange(0,float(len(x))/fs,1/fs)

		if (len(x)!=len(t)):
			x=x[:-1]

		fig1=Figure(figsize=(4,3),dpi=100)
		tplot=fig1.add_subplot(111)
		tplot.plot(t,x,linewidth=1,color="g")
		tplot.set_xlabel("Time [S]",labelpad=1)
		tplot.set_ylabel("Amplitude [a.u]",labelpad=2)
		tplot.set_title("Audio Signal")
		tplot.grid()
	
		canvasfig1=FigureCanvasTkAgg(fig1,master=imagesl)
		canvasfig1.draw()
		canvasfig1.get_tk_widget().place(relx=0,rely=0,relwidth=1,relheight=1)

	else:
    	#Display and error if none is found
		messagebox.showerror(message="First record something")
		txt.set("Off: Not Recording")
		record_label.config(fg="red")

def plot_ftime(y,fs):

	t=np.arange(0,len(y)/fs,1/fs)

	fig4=Figure(figsize=(4,3),dpi=100)
	faplot=fig4.add_subplot(111)
	faplot.plot(t,y,linewidth=1,color="g")
	faplot.set_xlabel("Time [S]",labelpad=1)
	faplot.set_ylabel("Amplitude [a.u]",labelpad=2)
	faplot.set_title("Filtered Audio Signal")
	faplot.grid()
	
	canvasfig4=FigureCanvasTkAgg(fig4,master=imageil)
	canvasfig4.draw()
	canvasfig4.get_tk_widget().place(relx=0,rely=0,relwidth=1,relheight=1)

def plot_filter3(H,fs):

	M=len(H)
	k=np.arange(0,M)
	fk=k*fs/M
	fig2=Figure(figsize=(4,3),dpi=100)

	freq=np.arange(0,2*np.pi,(2*np.pi)/M)
	angle=np.zeros(len(freq))

	fplot=fig2.add_subplot(211)
	fplot.plot(freq,np.real(H),linewidth=1,color="b",label="Magnitude")
	fplot.set_xlabel("f [Hz]",labelpad=2)
	fplot.set_ylabel("Magnitude",labelpad=1)
	#fplot.set_title("Filter Response")
	fplot.xaxis.set_label_position('top') 
	fplot.legend(loc="best")
	fplot.grid()

	ffplot=fig2.add_subplot(212)
	ffplot.plot(freq,angle,linewidth=1,color="r",label="Phase")
	ffplot.set_xlabel("f [Hz]",labelpad=1)
	ffplot.set_ylabel("Degree",labelpad=2)
	#ffplot.set_title("Audio Signal")
	ffplot.legend(loc="best")
	ffplot.grid()

	canvasfig2=FigureCanvasTkAgg(fig2,master=imagesr)
	canvasfig2.draw()
	canvasfig2.get_tk_widget().place(relx=0,rely=0,relwidth=1,relheight=1)

def plot_filter2(W,H,fs):

	Mag = 20*np.log10(abs(H))  
	Freq = W*fs/(2*np.pi)
	angles=np.unwrap(np.angle(H))

	fig2=Figure(figsize=(4,3),dpi=100)
	fplot=fig2.add_subplot(211)
	fplot.plot(Freq,Mag,linewidth=1,color="b",label="Magnitude")
	fplot.set_xlabel("f [Hz]",labelpad=3)
	fplot.set_ylabel("Magnitude [dB]",labelpad=2)
	#fplot.set_title("Filter Response")
	fplot.set_xlim(0,fs/2)
	fplot.xaxis.set_label_position('top') 
	fplot.legend(loc="best")
	fplot.grid()

	ffplot=fig2.add_subplot(212)
	ffplot.plot(W,angles,linewidth=1,color="r",label="Phase")
	ffplot.set_xlabel("f [Rad]",labelpad=1)
	ffplot.set_ylabel("Degree",labelpad=2)
	#ffplot.set_title("Audio Signal")
	ffplot.legend(loc="best")
	ffplot.grid()

	canvasfig2=FigureCanvasTkAgg(fig2,master=imagesr)
	canvasfig2.draw()
	canvasfig2.get_tk_widget().place(relx=0,rely=0,relwidth=1,relheight=1)

def plot_filter1(W,H,fs):
	
	w=(W-np.pi)*fs/(2*np.pi)
	h=np.abs(np.fft.fftshift(H))
	angles=np.unwrap(np.angle(H))

	fig2=Figure(figsize=(4,3),dpi=100)
	fplot=fig2.add_subplot(211)
	fplot.plot(w,h,linewidth=1,color="b",label="Magnitude")
	fplot.set_xlabel("f [Hz]",labelpad=3)
	fplot.set_ylabel("Magnitude [dB]",labelpad=2)
	#fplot.set_title("Filter Response")
	fplot.set_xlim(0,fs/2)
	fplot.xaxis.set_label_position('top') 
	fplot.legend(loc="best")
	fplot.grid()

	ffplot=fig2.add_subplot(212)
	ffplot.plot(W,angles,linewidth=1,color="r",label="Phase")
	ffplot.set_xlabel("f [Rad]",labelpad=1)
	ffplot.set_ylabel("Degree",labelpad=2)
	#ffplot.set_title("Audio Signal")
	ffplot.legend(loc="best")
	ffplot.grid()

	canvasfig2=FigureCanvasTkAgg(fig2,master=imagesr)
	canvasfig2.draw()
	canvasfig2.get_tk_widget().place(relx=0,rely=0,relwidth=1,relheight=1)

def plot_fft(y,fs,fc1,fc2):

	fc1=int(fc1)
	if (fc2==""):
		fc2=0
	else:
		fc2=int(fc2)
	
	dft=np.fft.fft(y)
	dft=abs(dft)
	freq_demod=np.fft.fftfreq(dft.size)*fs
	dft=dft/float(np.max(np.abs(dft)))
	dft=dft-np.mean(dft)
	fclimit=fc1+fc2+2000

	fig3=Figure(figsize=(4,3),dpi=100)
	fftplot=fig3.add_subplot(111)
	fftplot.semilogx(freq_demod,dft,linewidth=1,color="y")
	fftplot.set_xlabel("f [Hz]",labelpad=1)
	fftplot.set_ylabel("Magnitude",labelpad=2)
	#fftplot.set_xlim(0,fclimit)
	fftplot.set_title("Fast Fourier Tranform Output")
	fftplot.grid()

	canvasfig3=FigureCanvasTkAgg(fig3,master=imageir)
	canvasfig3.draw()
	canvasfig3.get_tk_widget().place(relx=0,rely=0,relwidth=1,relheight=1)

def error_message():
	messagebox.showerror(message="Please enter all the required parameters")

def calculate_filter(fc1,fc2,ripple,bw,ngain,window,band,firtype,iirtype,N,att):

	if file_exists:
		file_audio=('./audios/recording.wav')
		fs,x=read(file_audio)
		x=x/float(np.max(np.abs(x)))
		x=x-np.mean(x)

		if (method_cb.get()=="FIR"):
			if (firtype=="Windowing"):
				hwindow=ffir.fir_windowing(fs,band,window,bw,ripple,fc1,fc2,ngain)
				w_win,h_win=signal.freqz(hwindow,1,whole=True,worN=1024)
				plot_filter1(w_win,h_win,fs)
				filter_fir2(hwindow,x,fs,fc1,fc2)
			elif(firtype=="Freq. Sampling"):
				hfs=ffir.freq_sampling(fs,band,ngain,fc1,fc2)
				W,H=signal.freqz(hfs,1,whole=True,worN=1024)
				plot_filter2(W,H,fs)
				filter_fir(hfs,x,fs,fc1,fc2)
			elif(firtype=="Remez"):		
				hr=ffir.remezf(fs,ngain,bw,band,fc1,fc2)
				W,H=signal.freqz(hr,1,1024)
				plot_filter2(W,H,fs)
				filter_fir(hr,x,fs,fc1,fc2)
			else:
				messagebox.showerror(message="First select the FIR type")

		elif (method_cb.get()=="IIR"):
			z,p=fiir.analog_irr(fs,N,band,iirtype,fc1,fc2,att,ripple)
			W,H=signal.freqz(z,p,1024)
			plot_filter2(W,H,fs)
			filter_iir(z,p,x,fs,fc1,fc2)

		elif (method_cb.get()=="Ideal"):
			xf,H,Hf=fideal.clip(x,fs,band,fc1,fc2)
			plot_filter3(H,fs)
			filter_ideal(xf,fs,fc1,fc2)
		else:
			messagebox.showerror(message="First select the method")

	else:
		messagebox.showerror(message="First record something")

def save_filtered(y,fs):    
	#y must be float32                    
	y*=32767                              
	y16=np.int16(y)                      
	write("./audios/filtered.wav",fs,y16)    

def filter_fir2(hn,x,fs,fc1,fc2):                                            
	y=signal.lfilter(hn,1,x)       
	y=y/float(np.max(np.abs(y)))
	y=y-np.mean(y)	                                               
	plot_ftime(y,fs)                                                              
	plot_fft(y,fs,fc1,fc2)
	save_filtered(y,fs)  
                           
def filter_fir(hn,x,fs,fc1,fc2):                                            
	y=signal.lfilter(hn,1,x)                                                      
	plot_ftime(y,fs)                                                              
	plot_fft(y,fs,fc1,fc2)
	save_filtered(y,fs)                                                            
                                                                                   
def filter_iir(z,p,x,fs,fc1,fc2):
	y=signal.lfilter(z,p,x)
	plot_ftime(y,fs)                                                              
	plot_fft(y,fs,fc1,fc2)
	save_filtered(y,fs)                                                         
                                                                                   
def filter_ideal(xf,fs,fc1,fc2):                  
	rxf=np.real(xf)                      
	plot_ftime(rxf,fs)                    
	plot_fft(rxf,fs,fc1,fc2)
	save_filtered(rxf,fs)

def view_fc(event,fc2_label,fc2_input):
	if (type_cb.get()=="Lowpass" or type_cb.get()=="Highpass"):
		fc2_label.grid_forget()
		fc2_input.grid_forget()
	else:
		fc2_label.grid(row=9)
		fc2_input.grid(row=10)

def view_filters(event,Ngain_label,Ngain_input,window_label,window_cb,bw_label,bw_input,ripple_label,ripple_input):

	txt1=tk.StringVar()
	bw_label.config(textvariable=txt1)
	txt2=tk.StringVar()
	Ngain_label.config(textvariable=txt2)
	txt3=tk.StringVar()
	ir_label.config(textvariable=txt3)
	txt4=tk.StringVar()
	ripple_label.config(textvariable=txt4)


	global N_input, att_input
	if (method_cb.get()=="IIR"):
		Ngain_input.grid_forget()
		window_label.grid_forget()
		window_cb.grid_forget()
		bw_input.grid_forget()
		fir_cb.grid_forget()
		
		txt1.set("Filter Order")
		txt2.set("Attenuation [dB]")
		txt3.set("Select the IIR Method")
		txt4.set("Ripple %")

		ir_label.grid(row=5)
		iir_cb.grid(row=6)
		N_input.grid(row=16)
		att_input.grid(row=18)
		ripple_label.grid(row=13)
		ripple_input.grid(row=14)
		bw_label.grid(row=15)
		Ngain_label.grid(row=17)

	elif(method_cb.get()=="FIR"):
		ripple_label.grid(row=13)
		ripple_input.grid(row=14)
		Ngain_label.grid(row=17)
		Ngain_input.grid(row=18)
		window_label.grid(row=11)
		window_cb.grid(row=12)
		bw_label.grid(row=15)
		bw_input.grid(row=16)
		fir_cb.grid(row=6)
		ir_label.grid(row=5)

		txt1.set("Transition Band Width [Hz]")
		txt2.set("Gain [dB]")
		txt3.set("Select the FIR Method")
		txt4.set("Ripple %")

		N_input.grid_forget()
		att_input.grid_forget()
		iir_cb.grid_forget()
	else:
		window_label.grid_forget()
		window_cb.grid_forget()
		ripple_label.grid_forget()
		ripple_input.grid_forget()
		bw_label.grid_forget()	
		bw_input.grid_forget()
		Ngain_label.grid_forget()
		Ngain_input.grid_forget()
		N_input.grid_forget()
		att_input.grid_forget()
		ir_label.grid_forget()
		iir_cb.grid_forget()
		fir_cb.grid_forget()

def view_analog(event,Ngain_label,att_input,ripple_label,ripple_input):

	txt1=tk.StringVar()
	ripple_label.config(textvariable=txt1)

	if (iir_cb.get()=="Bessel" or iir_cb.get()=="Butterworth"):
		Ngain_label.grid_forget()
		att_input.grid_forget()
		ripple_label.grid_forget()
		ripple_input.grid_forget()

	elif (iir_cb.get()=="Chebyshev I"):
		Ngain_label.grid_forget()
		att_input.grid_forget()
		ripple_label.grid(row=13)
		ripple_input.grid(row=14)

		txt1.set("Ripple Attenuation [dB]")

	elif (iir_cb.get()=="Chebyshev II"):
		ripple_label.grid_forget()
		ripple_input.grid_forget()
		Ngain_label.grid(row=17)
		att_input.grid(row=18)

	elif (iir_cb.get()=="Elliptic"):
		ripple_label.grid(row=13)
		ripple_input.grid(row=14)
		Ngain_label.grid(row=17)
		att_input.grid(row=18)

		txt1.set("Ripple Attenuation [dB]")

def view_fir(event,window_label,window_cb,ripple_label,ripple_input,bw_label,bw_input,Ngain_label,Ngain_input):

	txt=tk.StringVar()
	Ngain_label.config(textvariable=txt)

	if (fir_cb.get()=="Freq. Sampling"):
		window_label.grid_forget()
		window_cb.grid_forget()
		bw_label.grid_forget()
		bw_input.grid_forget()
		ripple_label.grid_forget()
		ripple_input.grid_forget()
		txt.set("Filter Order")

	elif (fir_cb.get()=="Remez"):
		window_label.grid_forget()
		window_cb.grid_forget()
		ripple_label.grid_forget()
		ripple_input.grid_forget()

		bw_label.grid(row=15)
		bw_input.grid(row=16)


		txt.set("Filter Order")

	else:
		window_label.grid(row=11)
		window_cb.grid(row=12)
		ripple_label.grid(row=13)
		ripple_input.grid(row=14)
		bw_label.grid(row=15)
		bw_input.grid(row=16)
		txt.set("Gain [dB]")

#def help_geometry(filewin):
#w=600
#    h=400
#    ws = filewin.winfo_screenwidth()
#    hs = filewin.winfo_screenheight()
#    x = (ws/2) - (w/2)
#    y = (hs/2) - (h/2)
#    filewin.geometry('%dx%d+%d+%d' % (w, h, x, y))

def help_view():
    filewin = tk.Toplevel()
    filewin.title("Help")
    with open("./resources/help.txt",'r') as f:
        about_text=f.read()
        l=tk.Label(filewin,text=about_text,justify="left").pack(padx=8,pady=8,fill='both',expand=True)

def help_about():
    filewin = tk.Toplevel()
    filewin.title("About")
    #help_geometry(filewin)
    #hframe=tk.Frame(filewin).pack(fill="both",expand=True)
    with open("./resources/about.txt",'r') as f:
        about_text=f.read()
 #        l=tk.Label(hframe,text=about_text,justify="center").pack(fill='both',expand=True)
        l=tk.Label(filewin,text=about_text,justify="center").pack(padx=8,pady=8,fill='both',expand=True)

#Fit data into queue
def callback(indata, frames, time, status):
    q.put(indata.copy())

#Functions to play, stop and record audio
#The recording is done as a thread to prevent it being the main process
def threading_rec(x,record_label):

	txt=tk.StringVar()
	record_label.config(textvariable=txt)
	if (x==1):
		#If recording is selected, then the thread is activated
		txt.set("On: Recording Audio")
		record_label.config(fg="green")
		t1=threading.Thread(target= record_audio)
		t1.start()

	elif (x==2):
  		#To stop, set the flag to false
		global recording
		txt.set("Off: Not Recording")
		record_label.config(fg="red")
		recording = False
		messagebox.showinfo(message="Recording Finished")
		plot_time()

def start_play():
	if file_exists:
		#Read the recording if it exists and play it
		pygame.mixer.music.load("./audios/recording.wav")
		pygame.mixer.music.play(loops=0)
	else:
    	#Display and error if none is found
		messagebox.showerror(message="Record something to play")

def stop_play():
	pygame.mixer.music.stop()

def record_audio():
    #Declare global variables    
    global recording 
    #Set to True to record
    recording= True   
    global file_exists 
    #Create a file to save the audio
    messagebox.showinfo(message="Click OK to record audio")
    with sf.SoundFile("./audios/recording.wav", mode='w', samplerate=44100,
                        channels=1) as file:
    #Create an input stream to record audio without a preset time
            with sd.InputStream(samplerate=44100, channels=1, callback=callback):
                while recording == True:
                    #Set the variable to True to allow playing the audio later
                    file_exists =True
                    #write into file
                    file.write(q.get())

def start_filtered():
	pygame.mixer.music.load("./audios/filtered.wav")
	pygame.mixer.music.play(loops=0)

def stop_filtered():
	pygame.mixer.music.stop()

def export_data(fc1,fc2,ripple,bw,ngain,window,band,firtype,iirtype,N,att,method):

	dat=f'Method: {method}\nBand: {band}\nFIR filter: {firtype}\nIIR filter: {iirtype}\nFrequency cut 1: {fc1}\nFrequency cut 2: {fc2}\n Window: {window}\nFilter Order: {N}\nRipple: {ripple}\nTransition band width: {bw}\nGain [dB]: {ngain}\nAttenuation: [dB] {att}'

	files = [('All Files', '*.*'),('Dat Files', '*.dat'),('Text Document', '*.txt')]
	f = asksaveasfile(filetypes = files, defaultextension = files)
	f.write(dat)

#GUI Variables
#Create a queue to contain the audio data
q = queue.Queue()
#Declare variables and initialise them
recording = False
file_exists = False

pygame.mixer.init()

fmethods=('FIR','IIR','Ideal')
ftypes=('Bandpass','Bandstop','Highpass','Lowpass')
windows=('Default','Bartlett','Blackman','Hamming','Hann','Square')
firmethods=('Windowing','Freq. Sampling','Remez')
iirmethods=('Bessel','Butterworth','Chebyshev I','Chebyshev II','Elliptic')

#main window for the interface
window=tk.Tk()
window.tk.call('wm', 'iconphoto', window._w, tk.PhotoImage(file='./resources/icon.png'))
w=1300
h=900
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
window.geometry('%dx%d+%d+%d' % (w, h, x, y))
window.title("DSP Filter's Bank")

#menu
menubar = tk.Menu(window)

interfacemenu=tk.Menu(menubar,tearoff=0)
#interfacemenu.add_command(label="Clean Layout",command=clean_interface)
interfacemenu.add_command(label="Exit",command=window.quit)
menubar.add_cascade(label="File",menu=interfacemenu)

helpmenu=tk.Menu(menubar,tearoff=0)
helpmenu.add_command(label="Help", command=help_view)
helpmenu.add_command(label="About", command=help_about)
menubar.add_cascade(label="Help", menu=helpmenu)

window.config(menu=menubar)

#main frame
main=tk.Frame(window)
main.place(relx=0,rely=0,relwidth=1,relheight=1)
main.configure(bg='white')

#record audio wav
audioload_frame=tk.LabelFrame(main, text="Audio Input",font="bold")
audioload_frame.place(relx=0.22,rely=0.01,relwidth=0.5,relheight=0.16)
audioload_frame.configure(bg='white')

#Control of the playback
recording_frame=tk.LabelFrame(audioload_frame)
recording_frame.place(relx=0.01,rely=0.02,relwidth=0.48,relheight=0.96)
recording_frame.configure(bg='white')

listen_frame=tk.LabelFrame(audioload_frame)
listen_frame.place(relx=0.51,rely=0.02,relwidth=0.48,relheight=0.96)
listen_frame.configure(bg='white')

record_label=tk.Label(recording_frame,text="Off: Not Recording")
record_label.place(relx=0.05,rely=0.7)
record_label.configure(bg='white',fg="red",font='bold')

rec_btn=tk.Button(recording_frame,text="Record Audio",bg="#5d5e43",font="bold",fg="white",command=lambda m=1:threading_rec(m,record_label))
rec_btn.place(relx=0.05,rely=0.2,relwidth=0.4,relheight=0.4)

stop_btn=tk.Button(recording_frame,text="Stop Recording",bg="#5d5e43",font="bold",fg="white",command=lambda m=2:threading_rec(m,record_label))
stop_btn.place(relx=0.55,rely=0.2,relwidth=0.4,relheight=0.4)

play_btn=tk.Button(listen_frame,text="Play Recording",bg="#5d5e43",font="bold",fg="white",command=start_play)
play_btn.place(relx=0.05,rely=0.2,relwidth=0.4,relheight=0.4)

pause_btn=tk.Button(listen_frame,text="Stop Playing",bg="#5d5e43",font="bold",fg="white",command=stop_play)
pause_btn.place(relx=0.55,rely=0.2,relwidth=0.4,relheight=0.4)

#Output audio
filtered_frame=tk.LabelFrame(main, text="Results",font="bold")
filtered_frame.place(relx=0.74,rely=0.01,relwidth=0.25,relheight=0.16)
filtered_frame.configure(bg="white")

playf_btn=tk.Button(filtered_frame,text="Play Filtered",bg="#5d5e43",font="bold",fg="white",command=start_filtered)
playf_btn.place(relx=0.05,rely=0.2,relwidth=0.4,relheight=0.4)

pausef_btn=tk.Button(filtered_frame,text="Stop Playing",bg="#5d5e43",font="bold",fg="white",command=stop_filtered)
pausef_btn.place(relx=0.55,rely=0.2,relwidth=0.4,relheight=0.4)

#filter form
form=tk.LabelFrame(main,text="Input Design Parameters",font="bold")
form.place(relx=0.01,rely=0.01,relwidth=0.2,relheight=0.71)
form.configure(bg='white')

#global variables for responsive form
N_input=tk.Entry(form)
att_input=tk.Entry(form)

#Cut frequencies
fc1_label=tk.Label(form,text="Fc1 [Hz]",font="bold")
#fc1_label.place(relx=0.05,rely=0.16)
fc1_label.grid(row=7)
fc1_label.configure(bg='white')

fc1_input=tk.Entry(form)
#fc1_input.place(relx=0.05,rely=0.19,relwidth=0.4)
fc1_input.grid(row=8)

fc2_label=tk.Label(form,text="Fc2 [Hz]",font="bold")
#fc2_label.place(relx=0.05,rely=0.23)
fc2_label.grid(row=9)
fc2_label.configure(bg='white')

fc2_input=tk.Entry(form)
#fc2_input.place(relx=0.05,rely=0.26,relwidth=0.4)
fc2_input.grid(row=10)

#Window type
window_label=tk.Label(form,text="Select the Window Type",font="bold")
#window_label.place(relx=0.05,rely=0.51)
window_label.grid(row=11)
window_label.configure(bg='white')

window_str=tk.StringVar()
window_cb=ttk.Combobox(form,width=20,textvariable=window_str)
window_cb['state']='readonly'
window_cb['values']=windows
#window_cb.place(relx=0.05,rely=0.54)
window_cb.grid(row=12)
#window_cb.current(0)

#Ripple 
ripple_label=tk.Label(form,text="Ripple %",font="bold")
#ripple_label.place(relx=0.05,rely=0.3)
ripple_label.grid(row=13)
ripple_label.configure(bg='white')

ripple_input=tk.Entry(form)
#ripple_input.place(relx=0.05,rely=0.33,relwidth=0.4)
ripple_input.grid(row=14)

#Width of the transition band
bw_label=tk.Label(form,text="Transition Band Width [Hz]",font="bold")
#bw_label.place(relx=0.05,rely=0.44)
bw_label.grid(row=15)
bw_label.configure(bg='white')

bw_input=tk.Entry(form)
#bw_input.place(relx=0.05,rely=0.47,relwidth=0.4)
bw_input.grid(row=16)

#Gain or Filter order
Ngain_label=tk.Label(form,text="Gain [dB]",font="bold")
#gain_label.place(relx=0.05,rely=0.37)
Ngain_label.grid(row=17)
Ngain_label.configure(bg='white')

Ngain_input=tk.Entry(form)
#gain_input.place(relx=0.05,rely=0.4,relwidth=0.4)
Ngain_input.grid(row=18)

#Filter method combobox
method_label=tk.Label(form,text="Select the Method",font="bold")
#method_label.place(relx=0.05,rely=0.02)
method_label.grid(row=1,pady=(15,0))
method_label.configure(bg='white')

method_str=tk.StringVar()
method_cb=ttk.Combobox(form,width=20,textvariable=method_str)
method_cb['state']='readonly'
method_cb['values']=fmethods
#method_cb.place(relx=0.05,rely=0.05)
method_cb.grid(row=2)
#method_cb.current(0)
method_cb.bind("<<ComboboxSelected>>",lambda event: view_filters(event,Ngain_label,Ngain_input,window_label,window_cb,bw_label,bw_input,ripple_label,ripple_input))

#Filter type combobox
type_label=tk.Label(form,text="Select the Filter Band",font="bold")
#type_label.place(relx=0.05,rely=0.09)
type_label.grid(row=3)
type_label.configure(bg='white')

type_str=tk.StringVar()
type_cb=ttk.Combobox(form,width=20,textvariable=type_str)
type_cb['state']='readonly'
type_cb['values']=ftypes
#type_cb.place(relx=0.05,rely=0.12)
type_cb.grid(row=4)
#type_cb.current(0)
type_cb.bind("<<ComboboxSelected>>",lambda event: view_fc(event,fc2_label,fc2_input))

#FIR or IIR method
ir_label=tk.Label(form,text="Select the FIR Method",font="bold")
#ir_label.place(relx=0.05,rely=0.02)
ir_label.grid(row=5)
ir_label.configure(bg='white')

fir_str=tk.StringVar()
fir_cb=ttk.Combobox(form,width=20,textvariable=fir_str)
fir_cb['state']='readonly'
fir_cb['values']=firmethods
#ir_cb.place(relx=0.05,rely=0.05)
fir_cb.grid(row=6)
#fir_cb.current(0)
fir_cb.bind("<<ComboboxSelected>>",lambda event: view_fir(event,window_label,window_cb,ripple_label,ripple_input,bw_label,bw_input,Ngain_label,Ngain_input))

iir_str=tk.StringVar()
iir_cb=ttk.Combobox(form,width=20,textvariable=fir_str)
iir_cb['state']='readonly'
iir_cb['values']=iirmethods
#ir_cb.place(relx=0.05,rely=0.05)
#iir_cb.grid(row=6)
#iir_cb.current(0)
iir_cb.bind("<<ComboboxSelected>>",lambda event: view_analog(event,Ngain_label,att_input,ripple_label,ripple_input))

form.grid_columnconfigure(0,weight=1)

#graphics of interest
image_frame=tk.LabelFrame(main,text="Graphics of Interest",font="bold")
image_frame.place(relx=0.22,rely=0.18,relwidth=0.77,relheight=0.81)
image_frame.configure(bg='white')

imagesl=tk.LabelFrame(image_frame)
imagesl.place(relx=0.005,rely=0.005,relwidth=0.49,relheight=0.49)
imagesl.configure(bg='white')

imagesr=tk.LabelFrame(image_frame)
imagesr.place(relx=0.505,rely=0.005,relwidth=0.49,relheight=0.49)
imagesr.configure(bg='white')

imageil=tk.LabelFrame(image_frame)
imageil.place(relx=0.005,rely=0.505,relwidth=0.49,relheight=0.49)
imageil.configure(bg='white')

imageir=tk.LabelFrame(image_frame)
imageir.place(relx=0.505,rely=0.505,relwidth=0.49,relheight=0.49)
imageir.configure(bg='white')

#Frame calculate and save filter
results_frame=tk.LabelFrame(main,text="Calculate Filter",font="bold")
results_frame.place(relx=0.01,rely=0.72,relwidth=0.20,relheight=0.27)
results_frame.configure(bg='white')

btn_calculate=tk.Button(results_frame,text="Calculate",fg="white",bg="#5d5e43",font="bold",command=lambda:calculate_filter(fc1_input.get(),fc2_input.get(),ripple_input.get(),bw_input.get(),Ngain_input.get(),window_cb.get(),type_cb.get(),fir_cb.get(),iir_cb.get(),N_input.get(),att_input.get()))
btn_calculate.place(relx=0.2,rely=0.2,relwidth=0.6,relheight=0.2)

btn_save=tk.Button(results_frame,text="Export",fg="white",bg="#5d5e43",font="bold",command=lambda:export_data(fc1_input.get(),fc2_input.get(),ripple_input.get(),bw_input.get(),Ngain_input.get(),window_cb.get(),type_cb.get(),fir_cb.get(),iir_cb.get(),N_input.get(),att_input.get(),method_cb.get()))
btn_save.place(relx=0.2,rely=0.6,relwidth=0.6,relheight=0.21)

window.mainloop()
