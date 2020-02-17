from tkinter import *
from tkinter import ttk

def nextwrite(whatnext):
    print(detail_frame.winfo_children())
    for w in detail_frame.winfo_children():
        w.destroy()
    detail=ttk.Label(detail_frame, text=whatnext, width=40)
    detail.grid(row=0, column=0, pady=5)

def lastwrite():
    show_content("LAST")

def show_content(what_to_show):
    for w in content_frame.winfo_children():
        w.destroy()
    i=0
    while i < 7:
        month_label = ttk.Label(content_frame, text = what_to_show, width = 10)
        month_label.grid(row = 1, column = i, pady=5)
        i+=1

r=Tk()
r.geometry('1200x700+100+100')
r.title('My Own Reminder')
# r.configure(background="#111111")

mystyle = ttk.Style()
mystyle.configure("first.TFrame",background = 'blue')
mystyle.configure("second.TFrame", background = 'red')

left_frame = ttk.Frame(r, style="first.TFrame", width=100, height=100)
left_frame.grid_propagate(0)
right_frame = ttk.Frame(r, style="second.TFrame", width=200, height=200)
right_frame.grid_propagate(0)

left_frame.grid(row=0, column=0, sticky=N)
right_frame.grid(row=0, column=1)

ttk.Label(left_frame, text="left").grid(row=0)
ttk.Label(right_frame, text="right").grid(row=0)
'''
clock_frame = ttk.Frame(left_frame, style="first.TFrame")
detail_frame = ttk.Frame(left_frame)
clock_frame.grid(row=0, column=0)
detail_frame.grid(row=1, column=0)

clock = ttk.Label(clock_frame, text="CLOCK", width=40)
clock.grid(row=0, column=0, pady=5)


head_frame = ttk.Frame(right_frame, height=100, width=100)
content_frame = ttk.Frame(right_frame, height=100, width=100, )
head_frame.grid(row = 0, column = 0,)
content_frame.grid(row = 1, column = 0,)

last_button = ttk.Button(head_frame, text="NEXT", command = lambda: nextwrite("NEW Detail"))
last_button.grid(row = 0, column = 0)
year_label = ttk.Label(head_frame, text="2019-12", width=40, anchor = "center")
year_label.grid(row = 0, column = 1, pady=5)
last_button = ttk.Button(head_frame, text="LAST", command = lambda: show_content("LAST"))
last_button.grid(row = 0, column = 6)

show_content("Calendar")
nextwrite("Details")
'''
r.mainloop()