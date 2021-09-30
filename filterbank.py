import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

def plot_graphs():
	fig=Figure(figsize=(5,5),dpi=100)

	y=[i**2 for i in range(101)]

	plot1=fig.add_subplot(111)
	plot1.plot(y)
	plot1.grid()
	
	canvas=FigureCanvasTkAgg(fig,master=timeplot)
	canvas.draw()
	canvas.get_tk_widget().place(relx=0.03,rely=0.03,relwidth=0.94,relheight=0.94)

def view_fc(event,fc2_label,fc2_input):
	if (type_cb.get()=="Lowpass" or type_cb.get()=="Highpass"):
		fc2_label.grid_forget()
		fc2_input.grid_forget()
	else:
		fc2_label.grid(row=9,padx=(20,0),pady=(5,0))
		fc2_input.grid(row=10,padx=(20,0),pady=(5,0))


def view_ir(event,gain_label,gain_input,window_label,window_cb,bw_label,bw_input):
	if (method_cb.get()=="IIR"):
		gain_label.grid_forget()
		gain_input.grid_forget()
		window_label.grid_forget()
		window_cb.grid_forget()
		bw_label.grid_forget()
		bw_input.grid_forget()

		N_label=tk.Label(form,text="Filter Order")
		N_label.grid(padx=(25,0),pady=(5,0))

		N_input=tk.Entry(form)
		N_input.grid(padx=(25,0),pady=(5,0))

		att_label=tk.Label(form,text="Attenuation [dB]")
		att_label.grid(padx=(25,0),pady=(5,0))

		att_input=tk.Entry(form)
		att_input.grid(padx=(25,0),pady=(5,0))

	else:
		gain_label.grid(row=17,padx=(20,0),pady=(5,0))
		gain_input.grid(row=18,padx=(20,0),pady=(5,0))
		window_label.grid(row=11,padx=(20,0),pady=(5,0))
		window_cb.grid(row=12,padx=(20,0),pady=(5,0))
		bw_label.grid(row=15,padx=(20,0),pady=(5,0))
		bw_input.grid(row=16,padx=(20,0),pady=(5,0))

		N_label.grid_forget()
		N_input.grid_forget()
		att_label.grid_forget()
		att_input.grid_forget()

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
		window_label.grid(row=11,padx=(20,0),pady=(5,0))
		window_cb.grid(row=12,padx=(20,0),pady=(5,0))
		ripple_label.grid(row=13,padx=(20,0),pady=(5,0))
		ripple_input.grid(row=14,padx=(20,0),pady=(5,0))
		bw_label.grid(row=15,padx=(20,0),pady=(5,0))
		bw_input.grid(row=16,padx=(20,0),pady=(5,0))
		txt.set("Gain [dB]")

def help_view():
	filewin = tk.Toplevel(window)
	button = tk.Button(filewin, text="Do nothing button")
	button.pack()

def help_about():
	filewin = tk.Toplevel(window)
	button = tk.Button(filewin, text="Do nothing button")
	button.pack()

def clean_interface():
	filewin = tk.Toplevel(window)
	button = tk.Button(filewin, text="Do nothing button")
	button.pack()

#Window GUI

fmethods=('FIR','IIR')
ftypes=('Bandpass','Bandstop','Highpass','Lowpass')
windows=('Default','Bartlett','Blackmann','Hamming','Hann','Square')
firmethods=('Windowing','Freq. Sampling','Remez')
iirmethods=('Bessel','Butterworth','Chebyshev I','Chebyshev II','Elliptic')


#main window for the interface
window=tk.Tk()
w=1200
h=900
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
x = (ws/2) - (w/2)    
y = (hs/2) - (h/2)
window.geometry('%dx%d+%d+%d' % (w, h, x, y))
window.title("DSP Filter's Bank")

#menu
menubar = tk.Menu(window)

helpmenu=tk.Menu(menubar,tearoff=0)
helpmenu.add_command(label="Help", command=help_view)
helpmenu.add_command(label="About", command=help_about)
menubar.add_cascade(label="Help", menu=helpmenu)

interfacemenu=tk.Menu(menubar,tearoff=0)
interfacemenu.add_command(label="Clean",command=clean_interface)
menubar.add_cascade(label="Layout",menu=interfacemenu)

window.config(menu=menubar)

#main frame
main=tk.Frame(window)
main.place(relx=0,rely=0,relwidth=1,relheight=1)
main.configure(bg='white')

#load audio wav
audioload_frame=tk.LabelFrame(main, text="Audio Input")
audioload_frame.place(relx=0.01,rely=0.01,relwidth=0.23,relheight=0.25)

#filter form
form=tk.LabelFrame(main,text="Input Design Parameters")
form.place(relx=0.01,rely=0.28,relwidth=0.23,relheight=0.71)

#Cut frequencies
fc1_label=tk.Label(form,text="Fc1 [Hz]")
#fc1_label.place(relx=0.05,rely=0.16)
fc1_label.grid(row=7,padx=(25,0),pady=(5,0))

fc1_input=tk.Entry(form)
#fc1_input.place(relx=0.05,rely=0.19,relwidth=0.4)
fc1_input.grid(row=8,padx=(25,0),pady=(5,0))

fc2_label=tk.Label(form,text="Fc2 [Hz]")
#fc2_label.place(relx=0.05,rely=0.23)
fc2_label.grid(row=9,padx=(25,0),pady=(5,0))

fc2_input=tk.Entry(form)
#fc2_input.place(relx=0.05,rely=0.26,relwidth=0.4)
fc2_input.grid(row=10,padx=(25,0),pady=(5,0))

#Window type
window_label=tk.Label(form,text="Select the window Type")
#window_label.place(relx=0.05,rely=0.51)
window_label.grid(row=11,padx=(25,0),pady=(5,0))

window_str=tk.StringVar()
window_cb=ttk.Combobox(form,width=22,textvariable=window_str)
window_cb['state']='readonly'
window_cb['values']=windows
#window_cb.place(relx=0.05,rely=0.54)
window_cb.grid(row=12,padx=(25,0),pady=(5,0))
window_cb.current(0)

#Ripple 
ripple_label=tk.Label(form,text="Ripple %")
#ripple_label.place(relx=0.05,rely=0.3)
ripple_label.grid(row=13,padx=(25,0),pady=(5,0))

ripple_input=tk.Entry(form)
#ripple_input.place(relx=0.05,rely=0.33,relwidth=0.4)
ripple_input.grid(row=14,padx=(25,0),pady=(5,0))

#Width of the transition band
bw_label=tk.Label(form,text="Transition Band Width")
#bw_label.place(relx=0.05,rely=0.44)
bw_label.grid(row=15,padx=(25,0),pady=(5,0))

bw_input=tk.Entry(form)
#bw_input.place(relx=0.05,rely=0.47,relwidth=0.4)
bw_input.grid(row=16,padx=(25,0),pady=(5,0))

#Gain or Filter order
Ngain_label=tk.Label(form,text="Gain [dB]")
#gain_label.place(relx=0.05,rely=0.37)
Ngain_label.grid(row=17,padx=(25,0),pady=(5,0))

Ngain_input=tk.Entry(form)
#gain_input.place(relx=0.05,rely=0.4,relwidth=0.4)
Ngain_input.grid(row=18,padx=(25,0),pady=(5,0))

#First rows
#Filter method combobox
method_label=tk.Label(form,text="Select the Method")
#method_label.place(relx=0.05,rely=0.02)
method_label.grid(row=1,padx=(25,0),pady=(25,0))

method_str=tk.StringVar()
method_cb=ttk.Combobox(form,width=22,textvariable=method_str)
method_cb['state']='readonly'
method_cb['values']=fmethods
#method_cb.place(relx=0.05,rely=0.05)
method_cb.grid(row=2,padx=(25,0),pady=(5,0))
method_cb.current(0)
method_cb.bind("<<ComboboxSelected>>",lambda event: view_ir(event,gain_label,gain_input,window_label,window_cb,bw_label,bw_input))

#Filter type combobox
type_label=tk.Label(form,text="Select the Filter Band")
#type_label.place(relx=0.05,rely=0.09)
type_label.grid(row=3,padx=(25,0),pady=(5,0))

type_str=tk.StringVar()
type_cb=ttk.Combobox(form,width=22,textvariable=type_str)
type_cb['state']='readonly'
type_cb['values']=ftypes
#type_cb.place(relx=0.05,rely=0.12)
type_cb.grid(row=4,padx=(25,0),pady=(5,0))
type_cb.current(0)
type_cb.bind("<<ComboboxSelected>>",lambda event: view_fc(event,fc2_label,fc2_input))

#FIR or IIR method
ir_label=tk.Label(form,text="Select the FIR method")
#ir_label.place(relx=0.05,rely=0.02)
ir_label.grid(row=5,padx=(25,0),pady=(5,0))

fir_str=tk.StringVar()
fir_cb=ttk.Combobox(form,width=22,textvariable=fir_str)
fir_cb['state']='readonly'
fir_cb['values']=firmethods
#ir_cb.place(relx=0.05,rely=0.05)
fir_cb.grid(row=6,padx=(25,0),pady=(5,0))
fir_cb.current(0)
fir_cb.bind("<<ComboboxSelected>>",lambda event: view_fir(event,window_label,window_cb,ripple_label,ripple_input,bw_label,bw_input,Ngain_label,Ngain_input))

#graphics of interest
image_frame=tk.LabelFrame(main,text="Graphics of Interest")
image_frame.place(relx=0.25,rely=0.01,relwidth=0.74,relheight=0.80)

time_frame=tk.LabelFrame(image_frame,text="Time Domain")
time_frame.place(relx=0.01,rely=0.01,relwidth=0.48,relheight=0.98)

timeplot=tk.Frame(time_frame)
timeplot.place(relx=0.01,rely=0.01,relwidth=0.98,relheight=0.48)

filteredplot=tk.Frame(time_frame)
filteredplot.place(relx=0.01,rely=0.51,relwidth=0.98,relheight=0.48)

freq_frame=tk.LabelFrame(image_frame,text="Frequency Domain")
freq_frame.place(relx=0.51,rely=0.01,relwidth=0.48,relheight=0.98)

freqplot=tk.Frame(freq_frame)
freqplot.place(relx=0.01,rely=0.01,relwidth=0.98,relheight=0.48)

filterresponse=tk.Frame(freq_frame)
filterresponse.place(relx=0.01,rely=0.51,relwidth=0.98,relheight=0.48)

#play audio and export results
results_frame=tk.LabelFrame(main, text="Results")
results_frame.place(relx=0.25,rely=0.82,relwidth=0.74,relheight=0.17)

window.mainloop()
