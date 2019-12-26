import pymysql

class Conn:
    def __init__(self):
        self.Adderrs='127.0.0.1'
        self.user='root'
        self.pwd='123456'
        self.Database='linksoup'
        self.Conn = pymysql.connect(host=self.Adderrs,port=3306,user=self.user,password=self.pwd,db=self.Database,charset='utf8')
        self.strat='False'
    def getArgs(self): #获取初始数据
        """

        @return:
        """
        try:
            cur=self.Conn.cursor()  #获取游标
            sql="select task_keyword,task_result,task_Read from linksoup_task ORDER BY id desc LIMIT 4"
            cur.execute(sql) #执行Sql语句
            res=cur.fetchall() #获取所有结果
            if len(res)<1: #判断是否为空
                cur.close() #关闭连接
                return False
            else:
                cur.close()
                return res  #返回一个tuple
        except Exception as e:
            return e
    def upate_sql(self,keyword,result_html): #任务执行完成，更新状态#关键词,html位置,更改读取项
        """

        @param keyword:
        @return:
        """
        try:
            cur=self.Conn.cursor()
            sql="UPDATE linksoup_task SET task_state='False',task_result=%s,task_Read='查看报表' WHERE task_keyword=%s"
            value=(result_html,keyword)
            cur.execute(sql,value)
            cur.commit()
            cur.close()
        except Exception as e:
            return e
    def insert_task(self,keyword,Clear): #添加任务
        """

        @param keyword:
        @param Clear:
        @return:
        """
        try:
            cur=self.Conn.cursor()
            sql_tasl="insert into linksoup_task(task_keyword,task_Clear) value (%s,%s)"
            value=(keyword,Clear)
            cur.execute(sql_tasl,value)
            cur.close()
            return True
        except Exception as e:
            print(e)
    def getClear(self): #获取任务
        """

        @return:
        """
        cur=self.Conn.cursor()
        sql = "select task_keyword,task_Clear,task_result,task_state from linksoup_task where task_state='True'"
        cur.execute(sql)
        res=cur.fetchall()
        return res
    def instrt_data(self,keyword,title,commpany,orgin,salary):
        """

        @param keyword:
        @param title:
        @param commpany:
        @param orgin:
        @param salary:
        """
        try:
            cur2=self.Conn.cursor()
            sql_tasl = "insert into linksoup_data(data_keyword,data_title,data_company,data_region,data_salary) value (%s,%s,%s,%s,%s)"
            value = (keyword,title,commpany,orgin,salary)
            cur2.execute(sql_tasl, value)
        except Exception as e:
            print(e)
    def get_numebr(self,Like,keyword):#查看每个城市的招聘数量
        """

        @param Like:
        @param keyword:
        @return:
        """
        try:
            cur2=self.Conn.cursor()
            sql_select_result="select data_title,data_company,data_region from linksoup_data where data_region LIKE %s and data_keyword=%s and data_salary!=0"
            value =('%'+Like+'%',keyword)
            cur2.execute(sql_select_result,value)
            result=cur2.fetchall()
            if len(result) != 0:
                return len(result)
            else:
                return 0
        except Exception as e:
            return e
    def get_sum(self,Like,keyword): #获取薪资总和
        """

        @param Like:
        @param keyword:
        @return:
        """
        try:
            cur2 = self.Conn.cursor()
            sql_select_result = "select sum(data_salary) From linksoup_data where data_region Like %s and data_keyword=%s and data_salary!=0"
            value = ('%'+Like + '%',keyword)
            cur2.execute(sql_select_result, value)
            result = cur2.fetchall()
            return result
        except Exception as e:
            return e