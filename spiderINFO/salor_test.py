import time,aiohttp
from bs4 import BeautifulSoup
from conn import connfig
import asyncio
from aiomysql import create_pool
from Clean import dataCleaning

sem = asyncio.Semaphore(200)

def getSalar(salar): #
    """
    @param salar:获取一个str类型的，查找-的位置，返回一个数字
    @return:
    """
    try:

        salar_Year = str(salar)
        salar_index = salar_Year.index('-')
        salar_result = salar_Year[0:salar_index]
        return float(salar_result)

    except ValueError:
        num = 0
        return num

async def parset(url,keword):
    """

    @param url: 接收一个参数存放url
    @param keword:关键词
    """
    async with sem:  #设置读取数 win 509
        async with create_pool(host='127.0.0.1', port=3306, user='root', password='123456', db='linksoup') as aimysql: #设置链接信息并传给aimysl
            async with aimysql.get() as cour: #创建链接并传给cour
                async with cour.cursor() as cur:#获取游标
                    async with aiohttp.ClientSession() as sseion: #创建对象
                        async with sseion.get(url) as reson: #发送请求并将响应内容传递给reson
                            Text=await reson.text(encoding='gbk')
                            await loop.create_task(Down(Text,keword,cur))
async def Down(HTML,keyword,cur):
    # async with create_pool(host='127.0.0.1',port=3306,user='root',password='123456',db='linksoup') as aimysql:
    #     async with aimysql.get() as cour:
    #         async with cour.cursor() as cur:
        _salar_key_Tran = '万'
        __salar_key_More_1 = '年'
        args=BeautifulSoup(str(HTML),'lxml')
        title = '#resultList > div > p > span > a'
        company = '#resultList > div > span.t2 > a'
        orgin = '#resultList > div > span.t3'
        salar = '#resultList > div > span.t4'
        __title = args.select(title)
        __ccompany =  args.select(company)
        __orgin = args.select(orgin)
        __salar =  args.select(salar)
        for i in range(len(__title)):
            res_title=__title[i].get_text().strip()
            res_company=__ccompany[i].get_text().strip()
            res_salar=__salar[i+1].get_text().strip()
            if __salar_key_More_1 in res_salar:
                res_Num = getSalar(res_salar)
                Average = round(res_Num * 10000 / 12)
                res_salar  = str(Average).strip()
            else:  # 这是月
                if _salar_key_Tran in res_salar:  # 判断万
                        res_Num = getSalar(res_salar)
                        Average = round(res_Num * 10000)
                        res_salar = str(Average).strip()
                else:  # 这是千
                    res_Num = getSalar(res_salar)
                    Average = round(res_Num * 1000)
                    res_salar = str(Average).strip()
            res_orgin=__orgin[i+1].get_text().strip()
            sql_tasl = "insert into linksoup_data(data_keyword,data_title,data_company,data_region,data_salary) value (%s,%s,%s,%s,%s)"
            value = (keyword , res_title, res_company, res_orgin, res_salar)
            await cur.execute(sql_tasl,value)
                        # await csv_writer.writerow([res_title,res_company,res_salar,res_orgin,keyword])
async def main(loop,urls,keyword): #loop url地址,csv地址，关键词
        with open(urls) as f:
            result=[loop.create_task(parset(s.strip(),keyword))for s in f]
            await asyncio.wait(result)
if __name__ == '__main__':
    keyword = None
    Clear = None
    while True:
        Conn = connfig.Conn()
        Clear = Conn.getClear()
        if len(Clear) < 1:
            print("当前没有可执行任务")
            time.sleep(10)
            continue
        else:
            for i in Clear:
                print(i)
                keyword = str(i[0])
                __Clear = str(i[1])
                resu_Clear='../'+str(__Clear[2:-1]) #url存放地址
                resu_numbe=str(__Clear[7:-5])#文件名数字
                time1 = time.time()
                loop = asyncio.get_event_loop()
                loop.run_until_complete(main(loop,resu_Clear,keyword)) #loop url地址,csv地址，关键词
                print(time.time() - time1)
                time.sleep(3)
                print("正在生成报表")
                result_all_s,result_Avg =dataCleaning.get_Cler(keyword)
                result_html = "../static/HTML/" + str(resu_numbe) + ".html"
                dataCleaning.Viewhtml(keyword,result_all_s,result_Avg,result_html)
                Conn.upate_sql(keyword,result_html)
                print("任务结束")
            continue