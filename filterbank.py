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
	canvas.get_tk_widget().place(relx=0.05,rely=0.05,relwidth=0.90,relheight=0.90)


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
main.place(relx=0.01,rely=0.01,relwidth=0.99,relheight=0.99)

b3=tk.Button(window,text="Plot",command=plot_graphs,fg='white',bg='black')
b3.place(relx=0.10,rely=0.65,relwidth=0.4,relheight=0.15)


#graphics of interest
image_frame=tk.LabelFrame(main,text="Graphics of Interest")
image_frame.place(relx=0.60,rely=0,relwidth=0.38,relheight=0.99)

timeplot=tk.LabelFrame(image_frame,text="Time Domain")
timeplot.place(relx=0.025,rely=0.02,relwidth=0.95,relheight=0.30)

freqplot=tk.LabelFrame(image_frame,text="Frequency Domain")
freqplot.place(relx=0.025,rely=0.35,relwidth=0.95,relheight=0.30)

filterplot=tk.LabelFrame(image_frame,text="Filter Response")
filterplot.place(relx=0.025,rely=0.68,relwidth=0.95,relheight=0.30)


window.mainloop()
