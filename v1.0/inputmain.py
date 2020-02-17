from tkinter import *
from tkinter import ttk
from db import *
import datetime
##### 下面这个库 dateutil，很高效地取代datetime，有些功能很好用
##### datetime.timedelta只能解析weeks, days的天数日期，而dateutil.relativedelta可以解析months, years的日期
from dateutil.relativedelta import relativedelta

class input_act:

    def __init__(self, input_window):
        self.mainWindow = input_window
        self.pattern    = IntVar()


        ################################################################
        ##### 定义使用的Frame，一共3个Frame
        ##### headframe显示抬头
        ##### contentframe用来显示内容
        ##### bottomframe用来存放按钮
        ################################################################
        self.mainFrame = Frame(self.mainWindow)
        self.mainFrame.grid()

        self.headFrame = Frame(self.mainFrame, width = 900, height = 50, padx=10, pady=10)
        self.headFrame.grid_propagate(0)
        self.headFrame.grid(row = 0, column = 0)

        self.contentFrame = Frame(self.mainFrame, width = 900, height = 500, padx=10, pady=5)
        self.contentFrame.grid_propagate(0)
        self.contentFrame.grid(row = 1, column = 0)

        self.bottomFrame = Frame(self.mainFrame, width = 900, height = 50, padx=10, pady=5)
        self.bottomFrame.grid_propagate(0)
        self.bottomFrame.grid(row = 2, column = 0)

        ################################################################
        ##### 定义使用的控件
        ##### 选择周期后，利用self.pattern_selected函数，加载必要的控件
        ################################################################
        pattern_label = ttk.Label(self.headFrame, text="Remind Pattern: ")
        pattern_label.grid(row=0, column = 0, sticky=W)

        pattern_combo_value = [("Once" , 1), ("Repeatedly", 2)]
        self.once_radio         = Radiobutton(self.headFrame, 
                                    padx = 10, 
                                    text = pattern_combo_value[0][0],  
                                    value = pattern_combo_value[0][1], 
                                    variable = self.pattern, 
                                    command =lambda: self.pattern_select(self.once_radio))
        self.repeatedly_radio   = Radiobutton(self.headFrame, 
                                    text = pattern_combo_value[1][0],  
                                    value = pattern_combo_value[1][1], 
                                    variable = self.pattern,
                                    command =lambda: self.pattern_select(self.repeatedly_radio))
        self.once_radio.grid(row = 0, column =1)
        self.repeatedly_radio.grid(row = 0, column = 2)
        
    def pattern_select(self, args):
        if args["value"] == 1:
            onceselect(self.mainWindow, self.contentFrame, self.bottomFrame)
        else:
            repeatedlyselect(self.mainWindow, self.contentFrame, self.bottomFrame)

########################################################################
##### 如果选择了单次提醒，使用一下的Class
########################################################################
class onceselect:
    ##### 初始化
    def __init__(self, mainWindow, contentFrame, bottomFrame):
        self.mainWindow     = mainWindow
        self.contentFrame   = contentFrame
        self.bottomFrame    = bottomFrame
        self.input_date     = StringVar()
        self.input_act      = StringVar()
        self.msg_var        = StringVar()
        self.msg_var.set("")
        
        ##### 清除ContentFrame和bottomFrame中的所有控件
        for widget in self.contentFrame.winfo_children():
            widget.destroy()
        for widget in self.bottomFrame.winfo_children():
            widget.destroy()
        
        ##### 加载控件
        date_label = ttk.Label(self.contentFrame, text = "Remind Date")
        date_label.grid(row=0, column = 0, sticky = W)
        self.date_entry = ttk.Entry(self.contentFrame, textvariable = self.input_date)
        self.date_entry.grid(row = 1, column = 0, sticky = W)
        act_label = Label(self.contentFrame, text = "Remind Issue")
        act_label.grid(row=2, column = 0, sticky = W)
        self.act_entry = Entry(self.contentFrame, width = 60, textvariable = self.input_act)
        self.act_entry.grid(row = 3, column = 0)
        self.msg_label = ttk.Label(self.contentFrame,
                                   foreground = "red",
                                   textvariable = self.msg_var)
        self.msg_label.grid(row = 8, sticky = W)
        self.oncebutton()
    
    ##### 设置按钮
    def oncebutton(self):
        ##### 定义bottom的按钮 
        self.saveButton = Button(self.bottomFrame, 
                            text="SAVE", 
                            width=8, 
                            command = self.saveonce, 
                            )
        self.saveButton.grid(row = 0, column = 0)
        self.exitButton = Button(self.bottomFrame, 
                            text="EXIT",  
                            width=8, 
                            command = self.mainWindow.destroy)
        self.exitButton. grid(row=0, column = 1)

    ##### 单次活动保存
    ##### 保存前需要检验日期格式，提醒内容不能为空
    def saveonce(self):
        ##### 检验日期格式是否正确
        if datevalidate(self.input_date.get()):
            ##### 检查提醒内容是否不是空
            if emptyvalidate(self.input_act.get()):
                sql_save = ('insert Into activity (act_date, act_statement) Values (%s, %s)')
                ##### 保存数据
                try:
                    db().db_handle((sql_save, self.input_date.get(), self.input_act.get()))
                    self.msg_var.set("The remind is saved!")
                    self.input_date.set("")
                    self.input_act.set("")
                    self.date_entry.focus()
                except:
                    self.msg_var.set("Wrong Save")
                    self.date_entry.focus()
                
            ##### 提醒内容不为空的处理
            else:
                self.act_entry.focus()
                self.msg_var.set("Remind Issue could not be empty!")
        ##### 提醒日期格式不正确的提醒
        else:
            self.date_entry.focus()
            self.msg_var.set("Date Format is Wrong! Should be 'YYYY-MM-DD'")
        
        
########################################################################
##### 如果选择了重复提醒，使用以下的Class
########################################################################
class repeatedlyselect:

    def __init__(self, mainWindow, contentFrame, bottomFrame):
        self.mainWindow     = mainWindow
        self.contentFrame   = contentFrame
        self.bottomFrame    = bottomFrame
        self.start_date     = StringVar()
        self.inteval        = StringVar()
        self.input_date     = StringVar()
        self.input_act      = StringVar()
        self.days           = IntVar()
        self.repeattimes    = IntVar()
        self.msg_var        = StringVar()
        
        ##### 清除ContentFrame和bottomFrame中的所有控件
        for widget in self.contentFrame.winfo_children():
            widget.destroy()
        for widget in self.bottomFrame.winfo_children():
            widget.destroy()
        self.repeatedlybutton()
        
        ##### 加载控件
        date_label = ttk.Label(self.contentFrame, text = "Remind Date")
        date_label.grid(row=0, column = 0, sticky = W)
        self.date_entry = ttk.Entry(self.contentFrame,
                                    textvariable = self.input_date,
                                    width = 12)
        self.date_entry.grid(row = 1, column = 0, sticky = W)
        act_label = Label(self.contentFrame, text = "Remind Issue")
        act_label.grid(row=2, column = 0, sticky = W)
        self.act_entry = ttk.Entry(self.contentFrame,
                               width = 60,
                               textvariable = self.input_act)
        self.act_entry.grid(row = 3, column = 0, columnspan = 8, sticky = W)
        
        self.inteval_label = ttk.Label(self.contentFrame, text = "Remind Inteval")
        self.inteval_label.grid(row = 4, column = 0, sticky = W)
        self.inteval_combo = ttk.Combobox(self.contentFrame,
                                          values = ["Every Day", "Weekly", "Monthly", "Yearly", "Fixed Days"],
                                          textvariable = self.inteval,
                                          width = 10)
        self.inteval_combo.set("Select")  
        ############################################################
        ### self.inteval_combo.set("Select") 用来设置combobox的提示值，这个值不是可选内容。
        ### self.inteval_comb.current(0) 这样的用法是设定提示值为初始值。数值对应不同的内容，0 - 有效值
        ############################################################
        self.inteval_combo.grid(row = 5, column = 0, sticky = W)
        self.inteval_combo.bind('<<ComboboxSelected>>', self.inteval_selected)
        
        ttk.Label(self.contentFrame,
                  text = "Repeat Times",
                  ).grid(row = 6, column = 0, sticky = W)
        self.repeat_entry = ttk.Entry(self.contentFrame,
                                      width = 5,
                                      textvariable = self.repeattimes,)
        self.repeat_entry.grid(row = 7, column = 0, sticky = W)
        ttk.Label(self.contentFrame,
                  textvariable = self.msg_var,
                  foreground = "red",
                  ).grid(row = 8, column = 0, columnspan = 8, sticky = W)

    def repeatedlybutton(self):
        ##### 定义bottom的按钮 
        self.saveButton = Button(self.bottomFrame, 
                            text="SAVE", 
                            width=8, 
                            command = self.saverepeatedly, 
                            )
        self.saveButton.grid(row = 0, column = 0)
        self.exitButton = Button(self.bottomFrame, 
                            text="EXIT",  
                            width=8, 
                            command = self.mainWindow.destroy)
        self.exitButton. grid(row=0, column = 1)

    def saverepeatedly(self):
        ##### 定义一个内部函数，用来获取提醒的日期，并以list的格式保存
        ##### 如果list的长度为 1，则表示年度的提示，如果大于 1, 则以活动的形式保存
        ##### 传入的数据是一个tuple，（提醒日期，重复次数，间隔代码, 提醒内容）
        ##### 重复的次数可以是0 或者大于1,0表示总是每年提醒
        def allok(*args):
            ##### 定义一个初始的空list
            remind_date = []
            ##### 将提醒日期从Str转换成date形式
            input_date = datetime.datetime.strptime(args[0], "%Y-%m-%d").date()
            remind_date.append(input_date.isoformat())
            
            ##### 按照提醒的重复次数循环
            ##### 如果重复的次数是0,则表示总是每年提醒，不执行如下语句
            i=1
            while i < args[1]:
                ##### 每天提醒
                if args[2] == "D":
                    remind_date.append((input_date + datetime.timedelta(days = 1*i)).isoformat())
                ##### 每周提醒
                elif args[2] == "W":
                    remind_date.append((input_date + datetime.timedelta(days = 7*i)).isoformat())
                ##### 每月提醒
                elif args[2] == "M":
                    remind_date.append((input_date + relativedelta(months = i)).isoformat())
                ##### 每年提醒
                elif args[2] == "Y":
                    remind_date.append((input_date + relativedelta(years = i)).isoformat())
                ##### 固定天数提醒
                else:
                    remind_date.append((input_date + datetime.timedelta(days = args[2]*i)).isoformat())
                i += 1
            
            ##### 日期的数据在remind_date的list里面
            ##### 下面就可以保存数据到数据库了
            if len(remind_date) == 1:
                sql_save = ('insert Into annual (annual_date, annual_statement) Values (%s, %s)')
            else:
                sql_save = ('insert Into activity (act_date, act_statement) Values (%s, %s)')
            
            ##### 保存数据
            for eachdate in remind_date:
                db().db_handle((sql_save, eachdate, args[3]))
  
            self.msg_var.set("The remind is saved!")
            self.input_date.set("")
            self.input_act.set("")
            self.date_entry.focus()
            
        ##### 检验日期格式是否正确
        if datevalidate(self.date_entry.get()):
            ##### 检查提醒内容是否不是空
            if emptyvalidate(self.act_entry.get()):
                inteval_value = ["Every Day", "Weekly", "Monthly", "Yearly", "Fixed Days"]
                if self.inteval.get() in inteval_value:
                    if self.inteval.get() == "Every Day":
                        repeat_time = "D"
                    if self.inteval.get() == "Weekly":
                        repeat_time = "W"
                    if self.inteval.get() == "Monthly":
                        repeat_time = "M"
                    if self.inteval.get() == "Yearly":
                        repeat_time = "Y"
                    if self.inteval.get() == "Fixed Days":
                        if self.days.get() > 1:
                            repeat_time = int(self.days_entry.get())
                            if self.repeattimes.get() > 1:
                                allok(self.date_entry.get(), int(self.repeat_entry.get()), repeat_time, self.input_act.get())
                            else:
                                self.msg_var.set("Repeat Times should be greater than 1!")
                                self.repeat_entry.focus()
                        else:
                            self.msg_var.set("Inteval Day should be greater than 1!")
                            self.days_entry.focus()
                    else:
                        if self.inteval.get() == "Yearly":
                            self.msg_var.set("* If you choose yearly as inteval and enter '0' at 'Repeat Times', it will treat as forever. Such as a birthday.")
                            allok(self.date_entry.get(), int(self.repeat_entry.get()), repeat_time, self.input_act.get())
                        else:
                            if self.repeattimes.get() > 1:
                                allok(self.date_entry.get(), int(self.repeat_entry.get()), repeat_time, self.input_act.get())
                            else:
                                self.msg_var.set("Repeat Times should be greater than 1!")
                                self.repeat_entry.focus()
                else:
                    self.msg_var.set("Please select Inteval!")
                    self.inteval_combo.focus()

            ##### 提醒内容不为空的处理
            else:
                self.act_entry.focus()
                self.msg_var.set("Remind Issue could not be empty!")
        ##### 提醒日期格式不正确的提醒
        else:
            self.date_entry.focus()
            self.msg_var.set("Date Format is Wrong! Should be 'YYYY-MM-DD'")
            
    def sql_save(self):
        sql_save = ('insert Into activity (act_date, act_statement) Values (%s, %s)')
        ##### 保存数据
        try:
            db().db_handle((sql_save, self.input_date.get(), self.input_act.get()))
            self.msg_var.set("The remind is saved!")
            self.input_date.set("")
            self.input_act.set("")
            self.date_entry.focus()
        except:
            self.msg_var.set("Wrong Save")
            self.date_entry.focus()
    
    def inteval_selected(self, args):
        if self.inteval.get() == "Fixed Days":
            self.days_label = ttk.Label(self.contentFrame, text = "Days of Inteval")
            self.days_label.grid(row = 4, column = 1, sticky = W)

            self.days_entry = ttk.Entry(self.contentFrame,
                                       textvariable = self.days,
                                       width = 5)
            self.days_entry.grid(row = 5, column = 1, sticky = W)
        else:
            try:
                if self.days_label:
                    self.days_label.destroy()
                    self.days_entry.destroy()
            except:
                print("NO")
        if self.inteval.get() == "Yearly":
            self.msg_var.set("* If you choose yearly as inteval and enter '0' at 'Repeat Times', it will treat as forever. Such as a birthday.")
        else:
            self.msg_var.set("")

##### 测试日期格式的函数
def datevalidate(args):
    try:
        datetime.datetime.strptime(args, '%Y-%m-%d')
        return 1
    except ValueError:
        pass

##### 测试字符串输入是不是为空的函数
def emptyvalidate(args):
    if len(args) == 0:
        return None
    else:
        return 1

###################################################################
##### 主程序
###################################################################
def main():
    input_window = Tk()
    input_window.title("REMIND INPUT")
    input_window.resizable(width = False, height = False)

    input_act(input_window)
    input_window.mainloop()

if __name__ == "__main__":
    main()
