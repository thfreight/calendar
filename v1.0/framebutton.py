from tkinter import *
from tkinter import ttk

def nextwrite(whatnext):
    print(detail_frame.winfo_children())
    for w in detail_frame.winfo_children():
        w.destroy()
    detail=ttk.Label(detail_frame, text=whatnext, width=40)
    detail.grid(row=0, column=0, pady=5)

r=Tk()
r.geometry('1200x700+100+100')
r.title('My Own Reminder')

mystyle = ttk.Style()
mystyle.configure("first.TFrame",background = 'blue')
mystyle.configure("second.TFrame", background = 'red')

left_frame = ttk.Frame(r, style="first.TFrame", width=400, height=100)
left_frame.grid_propagate(0)
right_frame = ttk.Frame(r, style="second.TFrame", width=200, height=200)
right_frame.grid_propagate(0)

left_frame.grid(row=0, column=0, sticky=NSEW)
right_frame.grid(row=0, column=1)

ttk.Button(left_frame, text="Last").grid(row=0,column=0)
ttk.Label(left_frame, text="left", width=8 ).grid(row=0, column=1,)
ttk.Button(left_frame, text="rightside").grid(row=0, column=2)
left_frame.grid_columnconfigure(0, weight=1)
left_frame.grid_columnconfigure(2, weight=1)

r.mainloop()