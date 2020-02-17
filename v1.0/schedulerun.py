# 主窗口首先运行
# 在主窗口内创建一个新的线程，运行schedule
# 主窗口关闭，这个线程还在运行，会有出错信息，但是不影响整个过程
# 这样就能够实现自动刷新程序

import schedule
import time
from tkinter import *
from tkinter import ttk
import threading

class addlabel():
	def __init__(self, master):
		self.r = master
		self.c = StringVar()
		self.c.set("First Label")
		self.l = ttk.Label(self.r, textvariable = self.c)
		self.l.grid(row=0, column=0)
		t=threading.Thread(target = self.schedfun)
		t.start()
		
	def foo(self):
		self.c.set(self.p)
	
	def schedfun(self):
		self.p=1
		schedule.every(0.1).minutes.do(self.foo)
		while True:
			schedule.run_pending()
			self.p=self.p+1
			time.sleep(1)

r=Tk()
al=addlabel(r)

r.mainloop()

