import calendar
import datetime

class displaymonth:

    def __init__(self, display_year, display_month):
        self.display_calendar = calendar.TextCalendar(calendar.MONDAY)
        self.display_year       = display_year
        self.display_month      = display_month
        # self.display_current_month()

    def display_current_month(self):
        return self.display_this_month()
    
    def display_pre_month(self):
        if self.display_month == 1:
            self.display_year -= 1
            self.display_month = 12
        else:
            self.display_month -= 1
        print(self.display_year, self.display_month)
        self.display_this_month()
    
    def display_next_month(self):
        if self.display_month == 12:
            self.display_year += 1
            self.display_month = 1
        else:
            self.display_month +=1
        print(self.display_year, self.display_month)
        self.display_this_month()

    def display_this_month(self):
        self.month_day = []
        self.weekhead=[]
        self.weekhead=['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
        for wh in self.weekhead:
            self.month_day.append([wh, 0, 0])
        
        for i in self.display_calendar.itermonthdays(self.display_year, self.display_month):
            if i == datetime.datetime.now().day and self.display_month == datetime.datetime.now().month:
                self.month_day.append([i, 1, 0])
            else: 
                self.month_day.append([i, 0, 0])

        self.x = 0
        self.y = 0
        each_day = 0
        
        while each_day < len(self.month_day):
            if self.y < 7:
                pass
            else:
                self.y = 0
                self.x += 1
            self.month_day[each_day] += [self.x, self.y, self.display_year, self.display_month]    
            self.y += 1
            each_day += 1
        return self.month_day

'''
def main():
    c_y = datetime.datetime.now().year
    c_m = datetime.datetime.now().month
    cd = displaymonth(c_y, c_m)
    
    r=Tk()
    r.geometry('1200x700+100+50')
    r.title('Single Day Stype')
    r.configure(background="#1c1c1c")

    for j in cd.display_this_month():
        calcell.calcell(r, j)

    r.mainloop()

if __name__ == "__main__":
    main()
'''