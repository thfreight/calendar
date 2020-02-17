from datetime           import datetime

from clock        		import clock
from celmonth         	import showcalendar
from showremind        	import showremind
from layout 			import *

########################################################################
##### 主程序
########################################################################
def main():
	newlayout = layout()
	##### 调用时钟
	clock(newlayout.clock_frame)
	##### 调用当日提醒内容
	showremind(newlayout.remind_frame, datetime.now().date())
	##### 调用日历		
	showcalendar(newlayout.calendar_head_frame, 
					newlayout.calendar_content_frame, 
					newlayout.remind_frame,
				)	
	newlayout.main_window.mainloop()

if __name__ == "__main__":
    main()
