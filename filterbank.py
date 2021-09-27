import tkinter as tk
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


#main window for the interface
window=tk.Tk()
w=1200
h=900
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
x = (ws/2) - (w/2)    
y = (hs/2) - (h/2)
window.geometry('%dx%d+%d+%d' % (w, h, x, y))
window.title("PSD Filter's Bank")

#main frame
main=tk.Frame(window)
main.place(relx=0,rely=0,relwidth=1,relheight=1)
main.configure(bg='white')

b3=tk.Button(window,text="Plot",command=plot_graphs,fg='white',bg='black')
b3.place(relx=0.10,rely=0.65,relwidth=0.4,relheight=0.15)


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
