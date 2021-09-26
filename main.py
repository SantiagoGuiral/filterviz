import tkinter as tk


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

window.mainloop()
