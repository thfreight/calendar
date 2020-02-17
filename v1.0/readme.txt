这个项目是用来运行一个树莓派上的小程序，用来提醒自己每天需要做什么工作，年纪大了，确实记不得太多东西了。
这个项目使用python 3 + mysql数据库 编写，也可以运行在windows, linux, mcOS 上
该项目创建于2020年元月，创作人：孙闽


程序说明

db.py
    这个程序定义了一个class:db，处理所有数据库的操作，包括：
        数据查询 -- db_query
        数据操作 -- db_handle
            数据操作包括数据插入和数据修改
    
    程序中的main()有一些范例，如果使用这些函数
    使用时可以直接调用后直接使用方法：
        from db import *
        mydb = db()
        query_sql = ("SELECT * FROM activity", "")
        my_data = mydb.db_query(query_sql)
        print(my_data)

程序流程：
main.py
	|
	|----|
	|	 |----layout.py
	|	 |----db.py
	|	 |----monthdata.py
	|
	|------------clock.py
	|------------celmonth.py
	|------------showremind.py
	|
	|----inputmain.py   (另外一个独立程序，用来输入数据）
	
测试程序：
----schedulerun.py 
----framebutton.py

该项目子2020年元月启动以来，基本达到预期的设想，但是也产生一些新的问题，为了方便开发，故此决定该项目于2020-2-16截止现有的工作，设置版本号为V1.0
新问题如下：
1. 如何删除数据
2. 日期输入简化
3. 日历查询过后怎么样能够自动回到本月
4. 每天午夜日历更新当日后，提醒内容也要更新到当日
5. 增加版本说明
6. 日历周末和假期是否需要色彩变化

完成以上功能之后，定义为2.0版本

