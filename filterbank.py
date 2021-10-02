import tkinter as tk
import sounddevice as sd
import soundfile as sf
import queue
import threading
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

		fig=Figure(figsize=(4,3),dpi=100)
		tplot=fig.add_subplot(111)
		tplot.plot(t,x,linewidth=2,color="b")
		tplot.set_xlabel("Time [S]")
		tplot.set_ylabel("Amplitude [a.u]")
		#tplot.set_title("Audio Signal")
		tplot.grid()
	
		canvasfig1=FigureCanvasTkAgg(fig,master=audioplot)
		canvasfig1.draw()
		canvasfig1.get_tk_widget().place(relx=0,rely=0,relwidth=1,relheight=1)

	else:
    	#Display and error if none is found
		messagebox.showerror(message="First record something")
		txt.set("Off: Not Recording")
		record_label.config(fg="red")

def plot_ftime(y,fs):

	fig4=Figure(figsize=(4,3),dpi=100)
	faplot=fig.add_subplot(111)
	faplot.plot(t,x,linewidth=2,color="b")
	faplot.set_xlabel("Time [S]")
	faplot.set_ylabel("Amplitude [a.u]")
	#tplot.set_title("Audio Signal")
	faplot.grid()
	
	canvasfig4=FigureCanvasTkAgg(fig4,master=cplot)
	canvasfig4.draw()
	canvasfig4.get_tk_widget().place(relx=0,rely=0,relwidth=1,relheight=1)

def plot_filter3(H,Hf):

	fig3=Figure(figsize=(4,3),dpi=100)
	fplot=fig.add_subplot(111)
	fplot.plot(Hf,np.real(H),linewidth=2,color="b")
	fplot.set_xlabel("f [Hz]")
	fplot.set_ylabel("Magnitude")
	#tplot.set_title("Audio Signal")
	fplot.grid()

	canvasfig2=FigureCanvasTkAgg(fig3,master=freqplot)
	canvasfig2.draw()
	canvasfig2.get_tk_widget().place(relx=0,rely=0,relwidth=1,relheight=1)


def plot_filter2(W,H):

	Mag = 20*np.log10(abs(H))  
	Freq = W*fs/(2*np.pi)

	fig2=Figure(figsize=(4,3),dpi=100)
	fplot=fig.add_subplot(111)
	fplot.plot(Freq,Mag,linewidth=2,color="b")
	fplot.set_xlabel("f [Hz]")
	fplot.set_ylabel("Magnitude [dB]")
	#tplot.set_title("Audio Signal")
	fplot.grid()

	canvasfig2=FigureCanvasTkAgg(fig2,master=freqplot)
	canvasfig2.draw()
	canvasfig2.get_tk_widget().place(relx=0,rely=0,relwidth=1,relheight=1)

def plot_filter1(W,H,fs):
	
	w=(W-np.pi)*fs/(2*np.pi)
	h=np.abs(np.fft.fftshift(H))

	fig2=Figure(figsize=(4,3),dpi=100)
	fplot=fig.add_subplot(111)
	fplot.plot(WW,HH,linewidth=2,color="b")
	fplot.set_xlabel("f [Hz]")
	fplot.set_ylabel("Magnitude")
	#tplot.set_title("Audio Signal")
	fplot.grid()

	canvasfig2=FigureCanvasTkAgg(fig2,master=freqplot)
	canvasfig2.draw()
	canvasfig2.get_tk_widget().place(relx=0,rely=0,relwidth=1,relheight=1)

def plot_phase3(H,Hf):

	fig3=Figure(figsize=(4,3),dpi=100)
	pplot=fig.add_subplot(111)
	pplot.plot(Hf,np.angle(H),linewidth=2,color="b")
	pplot.set_xlabel("F [Hz]")
	pplot.set_ylabel("Angle [Rad]")
	#tplot.set_title("Audio Signal")
	fplot.grid()

	canvasfig3=FigureCanvasTkAgg(fig3,master=pplot)
	canvasfig3.draw()
	canvasfig3.get_tk_widget().place(relx=0,rely=0,relwidth=1,relheight=1)


def plot_phase2(z,p):

	w,h=signal.freqz(z,p,1024)
	angles=np.unwrap(np.angle(h))	

	fig3=Figure(figsize=(4,3),dpi=100)
	pplot=fig.add_subplot(111)
	pplot.plot(w,angles,linewidth=2,color="b")
	pplot.set_xlabel("F [Hz]")
	pplot.set_ylabel("Angle [Rad]")
	#tplot.set_title("Audio Signal")
	fplot.grid()

	canvasfig3=FigureCanvasTkAgg(fig3,master=pplot)
	canvasfig3.draw()
	canvasfig3.get_tk_widget().place(relx=0,rely=0,relwidth=1,relheight=1)

def plot_phase(hn):

	w,h=signal.freqz(hn)
	angles=np.unwrap(np.angle(h))	

	fig3=Figure(figsize=(4,3),dpi=100)
	pplot=fig.add_subplot(111)
	pplot.plot(w,angles,linewidth=2,color="b")
	pplot.set_xlabel("F [Hz]")
	pplot.set_ylabel("Angle [Rad]")
	#tplot.set_title("Audio Signal")
	fplot.grid()

	canvasfig3=FigureCanvasTkAgg(fig3,master=pplot)
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
				if (band=="" or window=="" or bw=="" or ripple=="" or fc1==""):
					error_message()
				else:
					hn=ffir.fir_windowing(fs,band,window,bw,ripple,fc1,fc2,ngain)
					w_win,h_win=signal.freqz(hn,1,whole=True,woN=1024)
					plot_filter1(w_win,h_win,fs)
					plot_phase(hn)
					filter_fir(hn,x,fs)
			elif(firtype=="Freq. Sampling"):
				if(band=="" or N=="" or fc1==""):
					error_message()
				else:
					hn=ffir.freq_sampling(fs,band,N,fc1,fc2)
					W,H=signal.freqz(hn,1,whole=True,worN=1024)
					plot_filter1(W,H,fs)
					plot_phase(hn)
					filter_fir(hn,x,fs)
			elif(firtype=="Remez"):		
				if (N=="" or bw =="" or band=="" or fc1==""):
					error_message()
				else:
					hn=ffir_remezf(fs,N,bw,band,fc1,fc2)
					W,H=signal.freqz(hn,1,1024)
					plot_filter1(W,H,fs)
					plot_phase(hn)
					filter_fir(hn,x,fs)

		elif (method_cb.get()=="IIR"):
			if (N=="" or band=="" or iirtype=="" or fc1==""):
				error_message()
			else:
				z,p=fiir.analog_irr(fs,N,band,iirtype,fc1,fc2,att,ripple)
				W,H=signal.freqz(z,p,1024)
				plot_filter2(W,H)
				plot_phase2(z,p)
				filter_irr(z,p,x,fs)

		elif (method_cb.get()=="Ideal"):
			if(band=="" or fc1==""):
				error_message()
			else:
				xf,H,Hf=fideal.clip(x,fs,band,fc1,fc2)
				plot_filter3(H,Hf)
				plot_phase3(H,Hf)
				filter_ideal(xf,fs)

	else:
    	#Display and error if none is found
		messagebox.showerror(message="First record something")
		txt.set("Off: Not Recording")
		record_label.config(fg="red")

def filter_fir(hn,x,fs):
	y=signal.lfilter(hn,1,x)
	plot_ftime(y,fs)
	write("./audios/filtered.wav",fs,y.astype(np.int16))
	filtered_file=True

def filter_iir(z,p,x,fs):
	y=signal.lfilter(z,p,x)
	plot_ftime(y,fs)
	write("./audios/filtered.wav",fs,y.astype(np.int16))
	filtered_file=True

def filter_ideal(xf,fs):
	plot_ftime(xf,fs)
	write("./audios/filtered.wav",fs,xf.astype(np.int16))
	filtered_file=True

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

		ir_label.grid(row=5)
		iir_cb.grid(row=6)
		N_input.grid(row=16)
		att_input.grid(row=18)
		ripple_label.grid(row=13)
		ripple_input.grid(row=14)

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

		txt1.set("Transition Band Width")
		txt2.set("Gain [dB]")
		txt3.set("Select the FIR Method")

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

	elif (iir_cb.get()=="Chebyshev I"):
		ripple_label.grid_forget()
		ripple_input.grid_forget()
		Ngain_label.grid(row=17)
		att_input.grid(row=18)

	elif (iir_cb.get()=="Elliptic"):
		ripple_label.grid(row=13)
		ripple_input.grid(row=14)
		Ngain_label.grid(row=17)
		att_input.grid(row=18)

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

"""
def clean_interface():
	filewin = tk.Toplevel(window)
	filewin.title("Clean")
	w=600
	h=400
	ws = filewin.winfo_screenwidth()
	hs = filewin.winfo_screenheight()
	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2)
	filewin.geometry('%dx%d+%d+%d' % (w, h, x, y))
"""

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
		txt.set("Off: Not Recording")
		record_label.config(fg="red")

def stop_play():
	pygame.mixer.music.stop()

def record_audio():
    #Declare global variables    
    global recording 
    #Set to True to record
    recording= True   
    global file_exists 
    #Create a file to save the audio
    messagebox.showinfo(message="Recording Audio")
    with sf.SoundFile("./audios/recording.wav", mode='w', samplerate=44100,
                        channels=2) as file:
    #Create an input stream to record audio without a preset time
            with sd.InputStream(samplerate=44100, channels=2, callback=callback):
                while recording == True:
                    #Set the variable to True to allow playing the audio later
                    file_exists =True
                    #write into file
                    file.write(q.get())

def start_filtered():
	if filtered_file:
		#Read the recording if it exists and play it
		pygame.mixer.music.load("./audios/filtered.wav")
		pygame.mixer.music.play(loops=0)
	else:
    	#Display and error if none is found
		messagebox.showerror(message="First calculate the filter")
		txt.set("Off: Not Recording")
		record_label.config(fg="red")

def stop_filtered():
	pygame.mixer.music.stop()


def export_data(fc1,fc2,ripple,bw,ngain,window,band,firtype,iirtype,N,att,method):

	data=f'Method: {method}\nBand: {band}\nFIR filter: {firtype}\nIIR filter: {iirtype}\nFrequency cut 1: {fc1}\nFrequency cut 2: {fc2}\n Window: {window}\nFilter Order: {N}\nRipple: {ripple}\nTransition band width: {bw}\nGain [dB]: {ngain}\nAttenuation: [dB] {att}'

	files = [('All Files', '*.*'),('Dat Files', '*.dat'),('Text Document', '*.txt')]
	f = asksaveasfile(filetypes = files, defaultextension = files)
	f.write(data)

#GUI Variables
#Create a queue to contain the audio data
q = queue.Queue()
#Declare variables and initialise them
recording = False
file_exists = False
filtered_exists = False

pygame.mixer.init()

fmethods=('FIR','IIR','Ideal')
ftypes=('Bandpass','Bandstop','Highpass','Lowpass')
windows=('Default','Bartlett','Blackmann','Hamming','Hann','Square')
firmethods=('Windowing','Freq. Sampling','Remez')
iirmethods=('Bessel','Butterworth','Chebyshev I','Chebyshev II','Elliptic')

#main window for the interface
window=tk.Tk()
window.tk.call('wm', 'iconphoto', window._w, tk.PhotoImage(file='./resources/icon.png'))
w=1250
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
audioload_frame=tk.LabelFrame(main, text="Audio Input")
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

rec_btn=tk.Button(recording_frame,text="Record Audio",bg="black",fg="white",command=lambda m=1:threading_rec(m,record_label))
rec_btn.place(relx=0.05,rely=0.2,relwidth=0.4,relheight=0.4)

stop_btn=tk.Button(recording_frame,text="Stop Recording",bg="black",fg="white",command=lambda m=2:threading_rec(m,record_label))
stop_btn.place(relx=0.55,rely=0.2,relwidth=0.4,relheight=0.4)

play_btn=tk.Button(listen_frame,text="Play Recording",bg="black",fg="white",command=start_play)
play_btn.place(relx=0.05,rely=0.2,relwidth=0.4,relheight=0.4)

pause_btn=tk.Button(listen_frame,text="Stop Playing",bg="black",fg="white",command=stop_play)
pause_btn.place(relx=0.55,rely=0.2,relwidth=0.4,relheight=0.4)

#Output audio
filtered_frame=tk.LabelFrame(main, text="Results")
filtered_frame.place(relx=0.74,rely=0.01,relwidth=0.25,relheight=0.16)
filtered_frame.configure(bg="white")

playf_btn=tk.Button(filtered_frame,text="Play Filtered",bg="black",fg="white",command=start_filtered)
playf_btn.place(relx=0.05,rely=0.2,relwidth=0.4,relheight=0.4)

pausef_btn=tk.Button(filtered_frame,text="Stop Playing",bg="black",fg="white",command=stop_filtered)
pausef_btn.place(relx=0.55,rely=0.2,relwidth=0.4,relheight=0.4)

#filter form
form=tk.LabelFrame(main,text="Input Design Parameters")
form.place(relx=0.01,rely=0.01,relwidth=0.2,relheight=0.71)
form.configure(bg='white')

#global variables for responsive form
N_input=tk.Entry(form)
att_input=tk.Entry(form)

#Cut frequencies
fc1_label=tk.Label(form,text="Fc1 [Hz]")
#fc1_label.place(relx=0.05,rely=0.16)
fc1_label.grid(row=7)
fc1_label.configure(bg='white')

fc1_input=tk.Entry(form)
#fc1_input.place(relx=0.05,rely=0.19,relwidth=0.4)
fc1_input.grid(row=8)

fc2_label=tk.Label(form,text="Fc2 [Hz]")
#fc2_label.place(relx=0.05,rely=0.23)
fc2_label.grid(row=9)
fc2_label.configure(bg='white')

fc2_input=tk.Entry(form)
#fc2_input.place(relx=0.05,rely=0.26,relwidth=0.4)
fc2_input.grid(row=10)

#Window type
window_label=tk.Label(form,text="Select the Window Type")
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
ripple_label=tk.Label(form,text="Ripple %")
#ripple_label.place(relx=0.05,rely=0.3)
ripple_label.grid(row=13)
ripple_label.configure(bg='white')

ripple_input=tk.Entry(form)
#ripple_input.place(relx=0.05,rely=0.33,relwidth=0.4)
ripple_input.grid(row=14)

#Width of the transition band
bw_label=tk.Label(form,text="Transition Band Width")
#bw_label.place(relx=0.05,rely=0.44)
bw_label.grid(row=15)
bw_label.configure(bg='white')

bw_input=tk.Entry(form)
#bw_input.place(relx=0.05,rely=0.47,relwidth=0.4)
bw_input.grid(row=16)

#Gain or Filter order
Ngain_label=tk.Label(form,text="Gain [dB]")
#gain_label.place(relx=0.05,rely=0.37)
Ngain_label.grid(row=17)
Ngain_label.configure(bg='white')

Ngain_input=tk.Entry(form)
#gain_input.place(relx=0.05,rely=0.4,relwidth=0.4)
Ngain_input.grid(row=18)

#Filter method combobox
method_label=tk.Label(form,text="Select the Method")
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
type_label=tk.Label(form,text="Select the Filter Band")
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
ir_label=tk.Label(form,text="Select the FIR Method")
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
image_frame=tk.LabelFrame(main,text="Graphics of Interest")
image_frame.place(relx=0.22,rely=0.18,relwidth=0.77,relheight=0.81)
image_frame.configure(bg='white')

audioplot=tk.LabelFrame(image_frame)
audioplot.place(relx=0.005,rely=0.005,relwidth=0.49,relheight=0.49)
audioplot.configure(bg='white')

freqplot=tk.LabelFrame(image_frame)
freqplot.place(relx=0.505,rely=0.005,relwidth=0.49,relheight=0.49)
freqplot.configure(bg='white')

pplot=tk.LabelFrame(image_frame)
pplot.place(relx=0.005,rely=0.505,relwidth=0.49,relheight=0.49)
pplot.configure(bg='white')

cplot=tk.LabelFrame(image_frame)
cplot.place(relx=0.505,rely=0.505,relwidth=0.49,relheight=0.49)
cplot.configure(bg='white')

#Frame calculate and save filter
results_frame=tk.LabelFrame(main,text="Calculate Filter")
results_frame.place(relx=0.01,rely=0.72,relwidth=0.20,relheight=0.27)
results_frame.configure(bg='white')

btn_calculate=tk.Button(results_frame,text="Calculate",fg="white",bg="black",command=lambda:calculate_filter(fc1_input.get(),fc2_input.get(),ripple_input.get(),bw_input.get(),Ngain_input.get(),window_cb.get(),type_cb.get(),fir_cb.get(),iir_cb.get(),N_input.get(),att_input.get()))
btn_calculate.place(relx=0.2,rely=0.2,relwidth=0.6,relheight=0.2)

btn_save=tk.Button(results_frame,text="Export",fg="white",bg="black",command=lambda:export_data(fc1_input.get(),fc2_input.get(),ripple_input.get(),bw_input.get(),Ngain_input.get(),window_cb.get(),type_cb.get(),fir_cb.get(),iir_cb.get(),N_input.get(),att_input.get(),method_cb.get()))
btn_save.place(relx=0.2,rely=0.6,relwidth=0.6,relheight=0.21)

window.mainloop()
