from tkinter    import *
from tkinter    import ttk
from db         import *
from datetime   import datetime, date

class showremind:

    def __init__(self, master, this_date):
        self.master     = master
        self.this_date  = this_date
        self.date_var = StringVar()

        for wedget in self.master.winfo_children():
            wedget.destroy()
            
        detail = ttk.Label(self.master, 
                            text="Reminder:", 
                            font=("Helvetica", 20), 
                            width = 30,
                            anchor = W)
        detail.grid(row=0, column = 0)

        
        self.remind_content()     
        
    ####################################################################
    ##### 从数据库调用当天的数据
    ##### 包括Activity和annual两个数据库
    ####################################################################
    def remind_data(self):
        self.all_remind = []
        sql_query = ("SELECT act_statement FROM calendar.activity where act_date = %s", self.this_date)
        self.sql_data = db().db_query(sql_query)
        for each in self.sql_data:
            self.all_remind.append(each[0])
            
        sql_query = ("SELECT annual_statement FROM calendar.annual where month(annual_date) = %s and day(annual_date) = %s; ", self.this_date.month, self.this_date.day)
        self.sql_data = db().db_query(sql_query)
        for each in self.sql_data:
            self.all_remind.append(each[0])
            
        return(self.all_remind)

    ####################################################################
    ##### 显示提醒的内容
    ####################################################################    
    def remind_content(self):
        
        ttk.Separator(self.master,
                      orient=HORIZONTAL,
                      ).grid(row=1, column = 0, sticky = "ew")
        
        all_widgets = self.master.winfo_children()
        for i in range(2, len(self.master.winfo_children())):
            all_widgets[i].destroy()

        self.date_label = ttk.Label(self.master,
                                    text = self.this_date,
                                    font = ("Helvetica", 16),
                                    )
        self.date_label.grid(row = 2, column = 0, sticky = W)
        
        if self.remind_data():
            p=2
            for whatshow in self.remind_data():
                ttk.Label(self.master,
                            text = str(p-1) + " - " + whatshow,
                            font = ("Helvetica", 14),
                            anchor = W).grid(row = p+1, column = 0, sticky = W)
                p +=1
        else:
            ttk.Label(self.master,
                        text = "No any remind this day!",
                        font = ("Helvetica", 14),
                        anchor = W).grid(row = 3, column = 0, sticky = W)
        
        if date.today() != self.this_date:

            self.this_date = date.today()
            self.date_label.after(120000, self.remind_content)

'''
def main():
    w=Tk()
    d = datetime.now().date()
    myremind = showremind(w, d)

    w.mainloop()

if __name__ == "__main__":
    main()
'''
