import requests
from bs4 import BeautifulSoup
import random
from flask import render_template
class Requests:
    def __init__(self,keword): #初始化定义，接收keyword关键词
        self.keyword = str(keword)
        self.city='000000'
        self.init_url = 'https://search.51job.com/list/'+self.city+',000000,0000,00,9,99,' + self.keyword + ',2,8.html'
        self.headers = {
            'Content-Type': 'text/html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.Res_page=None
        self.Thread_one ='Link/'+str((random.randint(111111, 999999))) + '.txt'

    def pageCount(self):#创建一个爬虫 去获取页面总数 返回一个数字
        sourceCode = requests.get(url=self.init_url, headers=self.headers)
        sourceCode.encoding = 'gbk'
        analysis = BeautifulSoup(sourceCode.text, 'lxml')
        Result = analysis.select('#resultList > div.dw_page > div > div > div > span:nth-child(3)')
        if type(Result) == list:
            for i in Result:
                res = i.get_text()
                self.Res_page=res[1:-4]
                return self.Res_page
    def generatePage(self): #URL管理,创建一个文本并追加写入。
        try:
            for i in range(1,int(self.Res_page)+1):
                res_URL='https://search.51job.com/list/'+self.city+',000000,0000,00,9,99,' + self.keyword + ',2,'+str(i)+'.html'
                with open(self.Thread_one,'a') as f:
                    f.write(res_URL+'\n')
            f.close()
            return render_template('result.html')
        except:
            return "进程出错"

    def getText(self):
        return self.Thread_one
