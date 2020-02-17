########################################################################
### 这个程序用来连接数据库，并做数据库的操作
### 操作包括：查询，插入，更改数据。
########################################################################
import mysql.connector
from mysql.connector import errorcode
from datetime import date

class db:
    
    def __init__(self):
        self.databaseRef = {
            'user'  	: 'pi',
            'password' 	: '123',
            'host'    	: '192.168.0.200',
            'database' 	: 'calendar',
            }

    ########## 从数据库查询数据###########################################
    ###
    ### 数据传输过来，在args里面
    ### 数据传输的格式：(sql语句，需要查询的条件)
    ### 例如：("SELECT * FROM activity WHERE id = %s", "1"), 
    ### 如果没有条件，则查询所有记录 ("SELECT * FROM activity", "")
    ###
    ####################################################################
    def db_query(self, args, **kuargs):
        sql_query = args[0]
        sql_condition = args[1:len(args)]

        self.cnx=mysql.connector.connect(**self.databaseRef)
        sql_cursor = self.cnx.cursor(buffered=True)   

        # 判断是否有条件，执行不同的查询语句
        if sql_condition[0] == '':
            sql_cursor.execute(sql_query)
        else:
            sql_cursor.execute(sql_query, sql_condition)

        # 获取查询的结果    
        sql_result = sql_cursor.fetchall()
        sql_cursor.close()
        self.cnx.close()
        # 返回结果
        return sql_result

    ########## 在数据库中处理数据##########################################
    ###
    ### 这个操作包括插入，更新数据
    ### 数据传输过来，在args里面
    ### 数据传输的格式：(sql语句，需要处理的各个数据)
    ### 例如：('INSERT INTO annual (annual_date, annual_statement) VALUES (%s, %s)', date(2012, 12, 2), "Change Bruce")
    ###
    ####################################################################
    def db_handle(self, args, **kwargs):
        sql_insert = args[0]
        sql_value =  args[1: len(args)]

        self.cnx=mysql.connector.connect(**self.databaseRef)
        sql_cursor = self.cnx.cursor()
        sql_cursor.execute(sql_insert, sql_value)
        self.cnx.commit()
        sql_cursor.close()
        self.cnx.close()

'''
def main():
    newdb = db()
    
    # 插入数据范例
    insert_sql  = (
        "INSERT INTO annual (annual_date, annual_statement) VALUES (%s, %s)"
    )
    newdb.db_handle((insert_sql,  date(2020, 1,2), "Change Bruce"))
    
    '# 查询数据范例
    query_sql = ("SELECT * FROM activity", "")
    my_data = newdb.db_query(query_sql)
    print(my_data)
    
    # 更新数据范例
    update_sql = ("UPDATE annual SET annual_date = %s, annual_statement = %s WHERE id = %s", date(2020, 1, 20), "Sun Ning Birthday", 2)
    newdb.db_handle(update_sql)


if __name__ == '__main__':
    main()
'''
