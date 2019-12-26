import requests
from bs4 import BeautifulSoup
from conn import connfig
from concurrent.futures import ProcessPoolExecutor
import time
import csv
import asyncio
from time import strftime,localtime

class asySpider:
    def __init__(self):
        """

        """
        # self.keyword=None
        self.__runStart__ = 'False'  # 结束值
        self.__overStart__ = 'True'  # 起始值
        self.__urlClear__ = 'None'  # url任务列表
        self.__title = 'None'  # 标题
        self.__company = 'None'  # 公司
        self.__Orgin = 'None'  # 地区
        self.__salar = 'None'  # 薪资
        self._salar_key_Tran = '万'
        self.__salar_key_More_1 = '年'
        self.__Lase='工作地点'
        self.__Lase_2='异地招聘'
    def requests(self,url):
        """

        @param url:
        @return:
        """
        headers = {
            'Content-Type': 'text/html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        Tx = requests.get(url=url, headers=headers)
        Tx.encoding = 'gbk'
        return Tx

    def getSalar(self, salar):
        """

        @param salar:
        @return:
        """
        try:
            salar_Year = str(salar)
            salar_index = salar_Year.index('-')
            salar_result = salar_Year[0:salar_index]
            return float(salar_result)  # 返回一个int数字
        except ValueError:
            num = 0
            return num
    async def soup(self,Clear,keyword,text):#Clear,keyword,text
            """

            @param Clear:
            @param keyword:
            @param text:
            """
            with open('../csv/'+Clear[8:-4]+'.csv','a',newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(["标题", "公司", "月薪","地址","关键词"])
                salr = asySpider()
                args = BeautifulSoup(text, 'lxml')
                title = '#resultList > div > p > span > a'
                company = '#resultList > div > span.t2 > a'
                orgin = '#resultList > div > span.t3'
                salar = '#resultList > div > span.t4'
                __title = args.select(title)
                __ccompany = args.select(company)
                __orgin = args.select(orgin)
                __salar = args.select(salar)
                for i in range(len(__title)):
                    self.__title = __title[i].get_text().strip()
                    self.__company = __ccompany[i].get_text().strip()
                    self.__orgin = __orgin[i].get_text().strip()
                    if self.__Lase in self.__orgin or self.__Lase_2 in self.__orgin: #数据清洗
                        self.__orgin = None
                    self.__salar = __salar[i].get_text().strip()
                    if self.__salar_key_More_1 in self.__salar:  # 判断年
                        if self._salar_key_Tran in self.__salar:  # 判断万
                            res_Num = salr.getSalar(self.__salar)
                            Average = round(res_Num * 10000 / 12)
                            self.__salar = str(Average).strip()
                    else:  # 这是月
                        if self._salar_key_Tran in self.__salar:  # 判断万
                            res_Num = salr.getSalar(self.__salar)
                            Average = round(res_Num * 10000)
                            self.__salar = str(Average).strip()
                        else:  # 这是千
                            res_Num = salr.getSalar(self.__salar)
                            Average = round(res_Num * 1000)
                            self.__salar = str(Average).strip()
                    #写入CSV
                    csv_writer.writerow([self.__title, self.__company, self.__salar, self.__orgin,keyword])
                f.close()#写入数据库
                # inert = connfig.Conn()
                # inert.instrt_data(keyword, self.__title, self.__company, self.__orgin, self.__salar)
                # # print(keyword, self.__title, self.__company, self.__orgin, self.__salar)


if __name__ == '__main__':
    cler = asyncio.get_event_loop()
    Pool=ProcessPoolExecutor(8)
    UrlDocker=[]
    run = asySpider()
    keyword = None
    Clear = None
    while True:
        Conn = connfig.Conn()
        Clear = Conn.getClear()
        if len(Clear) < 1:
            print("当前没有可执行任务")
            time.sleep(30)
            continue
        else:
            for i in Clear:
                print(i)
                time1 = strftime("%Y-%m-%d %H:%M:%S", localtime())  # 当前时间
                keyword = str(i[0])
                __Clear = str(i[1])
                Clear = '../' + __Clear[2:-1]
                with open(Clear, 'r') as f:
                    for j in f:
                        UrlDocker.append(j.strip())
                    for k in UrlDocker:
                        reson=Pool.submit(run.requests,k)
                        html=reson.result()
                        getText=html.text
                        cler.run_until_complete(run.soup(Clear,keyword,getText))
                        # url = j.strip()
                        # Text = run.requests(url)
                        # run.soup(keyword, Text)
                        # # Td=threading.Thread(target=run.requests,args=(url))
                        # # Td.run()
                    Pool.shutdown(wait=True)
                    Conn.upate_sql(keyword)
            time2 = strftime("%Y-%m-%d %H:%M:%S", localtime())  # 当前时间
            print("任务执行完毕")
            print(time1,time2)
            time.sleep(30)
            continue
