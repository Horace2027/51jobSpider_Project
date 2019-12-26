from flask import Flask
from flask import render_template
from spiderINFO import getPage
from flask import request
from conn import connfig
app = Flask(__name__)

@app.route('/serach',methods=["POST"])
def serach():
    keyword=request.form.get('phonecoo')
    run=getPage.Requests(keyword)#创建对象并传入参数
    run.pageCount()  #生成一个内置变量,res_page为页面总数
    res=run.generatePage() #生成页面,如正常完成，则True,遇错误则False
    Cler=run.Thread_one.encode('utf-8')
    up=connfig.Conn() #创建对象
    up.insert_task(keyword,str(Cler)) #写入数据
    return res   #返回结果
@app.route('/')
def hello_world():
    run=connfig.Conn()
    View=run.getArgs()
    if View==False:
        Vie="暂无相关数据"
        return render_template('index.html', mss=Vie)
    else:

        return render_template('index.html', msg=list(View))
        # return "hello"#

if __name__ == '__main__':
    app.run()
