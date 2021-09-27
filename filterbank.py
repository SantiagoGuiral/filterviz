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

def view_method(event):

	texto=tk.StringVar()
	met.config(textvariable=texto)
	if (method_cb.get()=="IIR"):
		texto.set("IIR")
	else:
		texto.set("FIR")

fmethods=('IIR','FIR')
ftypes=('Low-pass','High-pass','Bandpass','Stopband')
windows=('Default','Bartlett','Blackmann','Hamming','Hann','Square')

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

#main frame
main=tk.Frame(window)
main.place(relx=0,rely=0,relwidth=1,relheight=1)
main.configure(bg='white')

#load audio wav
audioload_frame=tk.LabelFrame(main, text="Audio Input")
audioload_frame.place(relx=0.01,rely=0.01,relwidth=0.38,relheight=0.17)

#filter form
form=tk.LabelFrame(main,text="Input Design Parameters")
form.place(relx=0.01,rely=0.19,relwidth=0.38,relheight=0.80)

form_left=tk.Frame(form)
form_left.place(relx=0.01,rely=0.01,relwidth=0.48,relheight=0.98)

form_right=tk.Frame(form)
form_right.place(relx=0.51,rely=0.01,relwidth=0.48,relheight=0.98)


#Filter method combobox
method_label=tk.Label(form_left,text="Select the Method")
method_label.place(relx=0.01,rely=0.01)

method_str=tk.StringVar()
method_cb=ttk.Combobox(form_right,width=15,textvariable=method_str)
method_cb['state']='readonly'
method_cb['values']=fmethods
method_cb.place(relx=0.01,rely=0.01)
method_cb.current(0)
method_cb.bind("<<ComboboxSelected>>",view_method)


#Filter type combobox
type_label=tk.Label(form_left,text="Select the Filter Type")
type_label.place(relx=0.01,rely=0.06)

type_str=tk.StringVar()
type_cb=ttk.Combobox(form_right,width=15,textvariable=type_str)
type_cb['state']='readonly'
type_cb['values']=ftypes
type_cb.place(relx=0.01,rely=0.06)
type_cb.current(0)

#Cut frequencies
fc1_label=tk.Label(form_left,text="Fc1 [Hz]")
fc1_label.place(relx=0.01,rely=0.11)

fc2_label=tk.Label(form_right,text="Fc2 [Hz]")
fc2_label.place(relx=0.01,rely=0.11)

fc1_input=tk.Entry(form_left)
fc1_input.place(relx=0.31,rely=0.11,relwidth=0.4)

fc2_input=tk.Entry(form_right)
fc2_input.place(relx=0.31,rely=0.11,relwidth=0.4)


#Ripple and gain dB
ripple_label=tk.Label(form_left,text="Ripple %")
ripple_label.place(relx=0.01,rely=0.16)

gain_label=tk.Label(form_right,text="Gain [dB]")
gain_label.place(relx=0.01,rely=0.16)

ripple_input=tk.Entry(form_left)
ripple_input.place(relx=0.31,rely=0.16,relwidth=0.4)

gain_input=tk.Entry(form_right)
gain_input.place(relx=0.31,rely=0.16,relwidth=0.4)


#Width of the transition band
bw_label=tk.Label(form_left,text="Transition Band Width")
bw_label.place(relx=0.01,rely=0.21)

bw_input=tk.Entry(form_right)
bw_input.place(relx=0.01,rely=0.21,relwidth=0.4)

#Window type
window_label=tk.Label(form_left,text="Select the window Type")
window_label.place(relx=0.01,rely=0.26)

window_str=tk.StringVar()
window_cb=ttk.Combobox(form_right,width=15,textvariable=window_str)
window_cb['state']='readonly'
window_cb['values']=windows
window_cb.place(relx=0.01,rely=0.26)
window_cb.current(0)




met=tk.Label(form_left,text="IIR")
met.place(relx=0.01,rely=0.4)
#Filter type combobox

#graphics of interest
image_frame=tk.LabelFrame(main,text="Graphics of Interest")
image_frame.place(relx=0.40,rely=0.01,relwidth=0.59,relheight=0.80)

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
results_frame.place(relx=0.40,rely=0.82,relwidth=0.59,relheight=0.17)

window.mainloop()
