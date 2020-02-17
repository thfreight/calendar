########################################################################
### 这个程序用来调用选中月份的数据
### 包括日历的星期抬头，当月的数据和为止
### last_month 用来计算上个月的年和月，并返回调用this_month产生数据
### next_month 用来计算下个月的年和月，并返回调用this_month产生数据
### this_month 用来返回选中年月的数据，供ttk日历显示
### 数据是7位的List，[天，是否今天，是否有活动，x坐标，y坐标，年，月]
### 比如[28, 0, 0, 5, 1, 2020, 1]，表示28日，不是今天也没活动，显示坐标（5，1），2020年1月
########################################################################

import calendar
from datetime import datetime
from db import *

class monthdata:

    def __init__(self, display_year, display_month):
        self.display_calendar   = calendar.TextCalendar(calendar.MONDAY)
        self.display_year       = display_year
        self.display_month      = display_month
    
	####################################################################
	### 这个函数用来生成上个月的数据
	### 返回上个月的年和月
	####################################################################
    def last_month(self):
        if self.display_month == 1:
            self.display_year 	-= 1
            self.display_month 	= 12
        else:
            self.display_month -= 1
        return(self.display_year, self.display_month)
        
	####################################################################
	### 这个函数用来生成下个月的数据
	### 返回下个月的年和月
	####################################################################
    def next_month(self):
        if self.display_month == 12:
            self.display_year 	+= 1
            self.display_month 	= 1
        else:
            self.display_month +=1
        return(self.display_year, self.display_month)

	####################################################################
	### 这个函数用来生成一个月的数据
	### 这个数据是以List的形式，[day, istoday, isactive, x, y, year, month]
	####################################################################
    def this_month(self):
        self.month_day 	= []									### 定义月份的日子
        self.act_day 	= []									### 定义有活动的日子
        self.weekhead	= []
        self.weekhead	= ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
        
        ##### 从数据库调用有活动的日子数据，并以list形式，保存在self.act_day
        ##### 包括活动和年活动的日子
        mydb = db()
        act_sql = ("SELECT act_date FROM calendar.activity where month(act_date) = %s and year(act_date) = %s;", self.display_month, self.display_year)
        act_data = mydb.db_query(act_sql)
        if act_data:
            for item in act_data:
                self.act_day.append(item[0].day)
                
        act_sql = ("SELECT annual_date FROM calendar.annual where month(annual_date) = %s;", self.display_month)
        act_data = mydb.db_query(act_sql)
        if act_data:
            for item in act_data:
                self.act_day.append(item[0].day)        

        ##### 生成数据形式 ############################################
        for wh in self.weekhead:                    			### 周天抬头处理
            self.month_day.append([wh, 0])
        
        for i in self.display_calendar.itermonthdays(self.display_year, self.display_month):
            if i == datetime.now().day and self.display_month == datetime.now().month and self.display_year == datetime.now().year:
                self.month_day.append([i, 1])
            else: 
                self.month_day.append([i, 0])

        ##### 这里的x，y，表示在ttk中显示日期的坐标 ##################
        self.x = 0
        self.y = 0
        each_day = 0
        
        while each_day < len(self.month_day):
            if self.month_day[each_day][0] in self.act_day:		### 是否有活动，有的话处理
                self.month_day[each_day] += [1]
            else: 
                self.month_day[each_day] += [0]
            
            if self.y < 7:
                pass
            else:
                self.y = 0
                self.x += 1
            self.month_day[each_day] += [self.x, self.y, self.display_year, self.display_month]    
            self.y += 1
            each_day += 1
        return self.month_day

##### 测试程序 #########################################################
'''
def main():
    c_y = datetime.now().year
    c_m = datetime.now().month
    cd = monthdata(c_y, c_m)
    print(cd.this_month())
    #cd.last_month()
    #print(cd.this_month())
    #cd.next_month()
    #cd.next_month()    
    #print(cd.this_month())

if __name__ == "__main__":
    main()
'''
