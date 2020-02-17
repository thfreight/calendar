from tkinter    import *
from tkinter    import ttk 
from datetime   import datetime
from clock      import doubledigit
from monthdata  import *
from showremind import showremind
from layout 	import *

import threading
import schedule
import time

########################################################################
### 这个Class用来显示日历，包括日历的抬头
### 引入的变量是两个Frame，head_frame显示抬头
### Content_frame用来显示日历的内容
########################################################################
class showcalendar:
    
    def __init__(self, head_frame, content_frame, remind_frame):
        self.head_frame  	= head_frame
        self.content_frame 	= content_frame
        self.remind_frame	= remind_frame
        self.display_year 	= datetime.now().year
        self.display_month 	= datetime.now().month

        ################################################################
        ### 设置这个Class所使用的色彩
        ################################################################
        self.fg_grey    = "#c0c0c0"
        self.fg_gold    = "#ffd700"
        self.bg_blue    = "#064676"
        self.bg_black   = "#1c1c1c"
        self.bg_green   = "#2f4f4f"

        ################################################################
        ### 设置这个Class所使用的ttk样式，主要是Button
        ################################################################
        self.cellstyle = ttk.Style()
        self.cellstyle.theme_use("classic")

        # 今天没活动，背景蓝色，字体白灰色
        self.cellstyle.configure("TodayWithoutActivity.TButton", 
                            background 	= self.bg_blue,  		#蓝色
                            foreground 	= self.fg_grey,       	#白灰色
                            font		='helvetica 16',
                            relief 		= "flat",
                            width 		= 3,
                            )
        self.cellstyle.map("TodayWithoutActivity.TButton",
                            foreground	= [('pressed', self.fg_grey), 
                                        ('active', self.fg_grey)],
                            background	= [('pressed', self.bg_blue), 
                                        ('disabled', self.bg_blue), 
                                        ('active', self.bg_blue)],
                            )
        # 今天有活动，背景蓝色，字体金色
        self.cellstyle.configure("TodayWithActivity.TButton", 
                            background = self.bg_blue,  		#蓝色
                            foreground = self.fg_gold, 
                            font='helvetica 16',
                            relief = "flat",
                            width = 3,
                            )
        self.cellstyle.map("TodayWithActivity.TButton",
                            foreground	=[('pressed', self.fg_gold), 
                                        ('active', self.fg_gold)],
                            background=[('pressed', self.bg_blue), 
                                        ('disabled', self.bg_blue), 
                                        ('active', self.bg_blue)],
                            )
        
        # 非今天没活动，背景灰黑色，字体白灰色
        self.cellstyle.configure("DayWithoutActivity.TButton", 
                            foreground = self.fg_grey,
                            background = self.bg_black,  
                            font='helvetica 16',
                            relief = "flat",
                            width = 3,
                            )           
        self.cellstyle.map("DayWithoutActivity.TButton",
                            foreground=[('pressed', self.fg_grey), 
                                        ('active', self.fg_grey)],
                            background=[('pressed', self.bg_black), 
                                        ('disabled', self.bg_black), 
                                        ('active', self.bg_black)]
                            )
        
        ###### 非今天有活动，背景灰黑色，字体金色 ###########################
        self.cellstyle.configure("DayWithActivity.TButton", 
                            foreground = self.fg_gold,
                            background = self.bg_black,  
                            font='helvetica 16',
                            relief = "flat",
                            width = 3,
                            )
        self.cellstyle.map("DayWithActivity.TButton",
                            foreground=[('pressed', self.fg_gold), 
                                        ('active', self.fg_gold)],
                            background=[('pressed', self.bg_black), 
                                        ('disabled', self.bg_black), 
                                        ('active', self.bg_black)]
                            )
                
        # 设置星期抬头格式，背景黄色，字体蓝色
        self.cellstyle.configure("Week.TButton", 
                            foreground = self.fg_grey,
                            background = self.bg_green,  
                            font='helvetica 16',
                            relief = "flat",
                            width = 3,
                            )
        self.cellstyle.map("Week.TButton",
                            foreground=[('pressed',		self.fg_grey), 
                                        ('active', 		self.fg_grey)],
                            background=[('pressed', 	self.bg_green), 
                                        ('disabled', 	self.bg_green), 
                                        ('active', 		self.bg_green)]
                            )
        ### 所有初始化完成#############################################

        ##### 首次调用抬头和日历
        self.display_content()
        
        ##### 增加新的线程，用来在0：00刷新日历
        self.newthread = threading.Thread(target = self.updatetime)
        self.newthread.start()
    
    ####################################################################
    ##### 新线程调用函数，设置每天午夜刷新日历
    ####################################################################
    def updatetime(self):
        schedule.every().day.at("00:00").do(self.display_content)
        while True:
            schedule.run_pending()
            time.sleep(10)
    
    ####################################################################
    ### 调用日历的抬头和单元
    ### 之前要把框架中的所有Widget都清除
    ####################################################################
    def display_content(self):
		##### 清除框架中的Widge
        for w in self.content_frame.winfo_children():
            w.destroy()
        ##### 调用日历抬头    
        self.calendar_head()
        ##### 调用日历单元
        self.calendar_data = monthdata(self.display_year, self.display_month).this_month()
        for self.each_day in self.calendar_data:
            calendar_content(self.content_frame, self.remind_frame, self.each_day).createcell()
        
        
    ####################################################################
    ### 这个函数用来相应表头上的"NEXT" 和 "LAST"按钮
    ####################################################################
    def month_select(self, args, **kwargs):
        if args: 
            self.calendar_data = monthdata(self.display_year, self.display_month).next_month()
        else:
            self.calendar_data = monthdata(self.display_year, self.display_month).last_month()
        self.display_year 	= self.calendar_data[0]
        self.display_month 	= self.calendar_data[1]
        self.calendar_data = monthdata(self.display_year, self.display_month).this_month()
        self.calendar_head()
        self.display_content()
        
    ####################################################################
    ### 这个函数用来相生存日历的抬头
    ####################################################################       
    def calendar_head(self):
        for w in self.head_frame.winfo_children():
            w.destroy()

        last_button = ttk.Button(self.head_frame, 
                        text="LAST", 
                        command = lambda: self.month_select(0))
        last_button.grid(row = 0, column = 0)
        year_label = ttk.Label(self.head_frame, 
                        text    = str(self.display_year) 
                                  + " - " 
                                  + doubledigit(self.display_month), 
                        anchor  = "center", 
                        font    = ("Helvetica", 24),)
        year_label.grid(row = 0, column = 1,)
        last_button = ttk.Button(self.head_frame, 
                        text="NEXT", 
                        command = lambda: self.month_select(1))
        last_button.grid(row = 0, column = 2)

########################################################################
###	创建一个Class，用来显示日历中的每个单元
### 很奇怪，如果不用一个Class，那么单元中的Button就不能显示日期
########################################################################
class calendar_content:

    def __init__(self, content_frame, remind_frame, calendar_data):
        self.content_frame 	= content_frame
        self.remind_frame 	= remind_frame
        self.each_day 		= calendar_data

        if self.each_day[0] == 0:
            self.display_day 	= ""
        else:
            self.display_day 	= self.each_day[0]
        self.istoday      		= self.each_day[1]
        self.isactivity   		= self.each_day[2]
        self.cellx     			= self.each_day[3]
        self.celly         		= self.each_day[4]
        self.display_year		= self.each_day[5]
        self.display_month 		= self.each_day[6]

    def createcell(self):
        if isinstance(self.display_day, int):       			# 首先判断日期是不是数字？是的话向下执行
            if self.istoday == 1:                   			# 在判断这个日期是不是今天？
                self.cellistoday()
            else:
                self.cellisnormal()
        else:                                       			# 如果日期不是数字，向下执行
            if self.display_day == "":              			# 日期是不是为空，空表示日期格，但是没有数据
                self.cellisnormal()
            else:
                self.cellisweekhead()                 			# 日期不是数字，也不为空，则显示星期抬头
    
    ####################################################################
    ##### 点击日期单元时，执行如下函数
    ####################################################################
    def dayactivity(self, args, **kwargs):
        self.selected_date = datetime(
								year 	= self.display_year, 
								month 	= self.display_month, 
								day		= args).date()
	
        showremind(self.remind_frame, self.selected_date)

    # 显示日历的星期抬头
    def cellisweekhead(self):
        self.daycell = ttk.Button(self.content_frame, text=self.display_day, style = "Week.TButton")
        self.daycell.grid(row=self.cellx, column = self.celly)

    ##### 如果日期是今天 ##############################################
    def cellistoday(self):
        ##### 如果这天有提示或者活动 ##################################
        if self.isactivity == 1:
            self.daycell = ttk.Button(self.content_frame, 
                                    text=self.display_day, 
                                    style = "TodayWithActivity.TButton",
                                    command = lambda:self.dayactivity(self.display_day),
                                    )
        ##### 如果今天没活动 ##########################################
        else:
            self.daycell = ttk.Button(self.content_frame, 
                                    text=self.display_day, 
                                    style = "TodayWithoutActivity.TButton",
                                    command = lambda:self.dayactivity(self.display_day),
                                    )
        self.daycell.grid(row=self.cellx, column = self.celly)

    ##### 如果日期不是今天 ############################################
    def cellisnormal(self):
        # 如果这天有提示或者活动
        if self.isactivity == 1:
            self.daycell = ttk.Button(self.content_frame, 
                                    text=self.display_day, 
                                    style = "DayWithActivity.TButton",
                                    command = lambda:self.dayactivity(self.display_day),
                                    )
        # 如果这天没活动
        else:     
            self.daycell = ttk.Button(self.content_frame, 
                                    text=self.display_day, 
                                    style = "DayWithoutActivity.TButton",
                                    command = lambda:self.dayactivity(self.display_day),
                                    )
        self.daycell.grid(row=self.cellx, column = self.celly)
'''
##############################################################
### 以下是测试程序，用来单独调试以上Class使用
### 正式使用时必须要屏蔽掉才行
##############################################################

def main():
    r=Tk()
    r.geometry('1200x700+100+100')
    r.title('Single Day Stype')
    r.configure(background="#1c1c1c")

    f1 = ttk.Frame(r)
    f1.grid(row=0)
    f2=ttk.Frame(r)
    f2.grid(row=1)
    showcalendar(f1, f2)
    r.mainloop()

if __name__ == "__main__":
    main()
'''
