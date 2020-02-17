#############################################
### 这是显示时钟的子程序
#############################################
from datetime   import datetime
from tkinter    import *
from tkinter    import ttk

class clock:

    def __init__(self, master):
        self.datelable = ttk.Label(master, 
                                   font=("Helvetica", 24),)
        self.datelable.grid(row = 0, column = 0)

        self.timelabel = ttk.Label(master, 
                                   font = ("Helvetica", 72),)
        self.timelabel.grid(row = 1, column=0)
        self.update_label()

    def update_label(self):
        self.datelable.configure(text = 
                                 str(datetime.now().year) 
                                 + '-' 
                                 + doubledigit(datetime.now().month) 
                                 + '-' 
                                 + doubledigit(datetime.now().day))
        self.timelabel.configure(text = 
                                 doubledigit(datetime.now().hour) 
                                 + ':' 
                                 + doubledigit(datetime.now().minute))
        self.timelabel.after(1000, self.update_label)   # call this method again in 1,000 milliseconds

### 用来把数字设置成两位的字符格式
def doubledigit(a):
    doublea = "{0:0=2d}".format(int(a))
    return doublea

'''
def main():
    r=Tk()
    r.geometry('1200x700+100+100')
    r.title('My Own Reminder')
    r.configure(background="#111111")
    # r.overrideredirect(True) # 隐藏窗口的标题行
    clock(r)
    r.mainloop()

if __name__ == "__main__":
    main()
'''
