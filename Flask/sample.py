import os
import sqlite3
from flask import Flask, request, escape, render_template, make_response, jsonify
import pandas as pd

os.environ["FLASK_ENV"] = "development"
app = Flask(__name__)

#HTMLはpathから取得して表示させる(テンプレート)

@app.route("/") #ここを改変して機能を実装していく
def hello():
    return render_template("send.html") #templatesディレクトリから指定のを持ってくる

@app.route("/japan/<city>") #ここを改変して機能を実装していく
def japan(city):
    return render_template("hello.html", city=city) #html側の変数cityにcityを代入という意味

@app.route("/submit", methods=['POST'])
def submit():
    file = request.files['uploadFile']
    df = pd.read_csv(file)
    df.culums=['学籍番号','学生氏名','科目番号','科目名','単位数','春学期','秋学期','総合評価','科目区分','開講年度','開講区分']
    dbname='mysample.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    df.to_sql('sample', conn, if_exists='replace')
    select_sql = 'SELECT * FROM sample'
    rows = "<h1>履修データ</h1>"
    for row in cur.execute(select_sql):
        rows = rows + "<p>{}</p>".format(escape(row))
    cur.close()
    conn.close()
    #return rows>>>>>>データの表示
    return make_response(jsonify({'result':'upload OK.'})) #upload完了

doc = "<DOCTYPE html>"
doc += "<html><head><title>卒業要件確認アプリケーション</title></head><body><h1>確認結果</h1>"
    #------------------------------------------------------------
    #必修科目の判定
def decision(name,kamoku,need):
    dbname = 'mysample.db'   #DBを指定
    conn = sqlite3.connect(dbname) 
    cur = conn.cursor() 
    number=0
    global doc
    for row in cur.execute(kamoku):
        number+=row[0]
    if number<need:
        lack=need-number
        doc += "<p><b>{}</b>の単位が<b>{}単位足りていません</b>。</p>".format(name, lack)
    else:
        doc += "<p><b>{}</b>の単位は十分です。</p>".format(name)
    cur.close() 
    conn.close()

@app.route("/result")
def result():
    #体育(2)
    global doc
    pe='SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 like "2%";'
    decision('体育',pe,2)
    #総合(1)
    sougou='SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 in ("1207011","1210221","1210231","1221011","1222021","1224021") or 科目番号 like "1226%" or 科目番号 like "14%";'
    decision('学士基盤科目',sougou,1)
    #フレッシュマンセミナー(1)
    furesemi='SELECT 単位数 FROM sample WHERE 総合評価="P"  and 科目番号 like "11%";'
    decision('フレッシュマン・セミナー',furesemi,1)
    #誘い(1)
    izanai='SELECT 単位数 FROM sample WHERE 総合評価="P" and 科目番号 like "12276%";'
    decision('学問への誘い',izanai,1)
    #英語(4)
    english='SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 like "3%";'
    decision('英語',english,4)
    #情報(4)
    information='SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 like "6%";'
    decision('情報',information,4)
    #知識情報概論(1)
    cjg='SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 like "GA141%";'
    decision('知識情報概論',cjg,1)
    #アカスキ(1)
    akasuki='SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 like "GE121%";'
    decision('アカデミックスキルズ',akasuki,1)
    #プロ入(3)
    pronyu='SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 like "GA181%" or 科目番号 like "GE106%";'
    decision('プログラミング入門',pronyu,3)
    #情報数学A(2)
    josuA='SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号="GA15141" or 科目番号="GE10811";'
    decision('情報数学A',josuA,2)
    #cje1(2)
    cje1='SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 like "GE110%";'
    decision('知識情報演習Ⅰ',cje1,2)
    #cje2(2)
    cje2='SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 like "GE111%";'
    decision('知識情報演習Ⅱ',cje2,2)
    #cje3(2)
    cje3='SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 like "GE112%";'
    decision('知識情報演習Ⅲ',cje3,2)
    #専門英語A(2)
    seneiA='SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 like "GE116%" or 科目番号 like "GE117%";'
    decision('専門英語A',seneiA,2)
    #哲学(2)
    tetsu='SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号="GE10201";'
    decision('哲学',tetsu,2)
    #統計(2)
    tokei='SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号="GE10911";'
    decision('統計',tokei,2)
    #主専攻実習(2)
    syusenkou='SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 like "GE601%" or 科目番号 like "GE701%" or 科目番号 like "GE801%";'
    decision('主専攻実習',syusenkou,2)
    #専門英語BC(2)
    seneiBC='SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 like "GE507%" or 科目番号 like "GE508%";'
    decision('専門英語BC',seneiBC,2)
    #卒業研究(6)
    sotsuken='SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 like "GE510%";'
    decision('卒業研究',sotsuken,6)

    #自由単(GE7)(16～)
    freecredit7 = 'SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 like "GE7%";'
    decision('主専攻の専門科目',freecredit7,16)

    #自由単(GA4,GE4,GE6,GE8)(8～)
    freecreditno7 = 'SELECT 単位数  FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 like "GE7%";'
    decision('主専攻以外の専門科目',freecreditno7,8)

    #自由単(GA1,GE2,GE3)(32～52)
    freecredit123 = 'SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 like "GA%" or 科目番号 like "GE2%" or 科目番号 like "GE3%";'
    decision('専門基礎科目',freecredit123,32)

    #Gじゃない自由単(6～)
    free='SELECT 単位数  FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 not in ("G%","1%","2%","3%","4%","5%","6%","7%","8%","9%");'
    decision('他の学類の専門基礎科目',free,6)

    #教職を除いたすべての単位数
    allcredit='SELECT 単位数  FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 not like "9%";'
    num=0
    dbname = 'mysample.db'   #DBを指定
    conn = sqlite3.connect(dbname) 
    cur = conn.cursor() 
    for row in cur.execute(allcredit):
        num+=row[0]
        L=124-num
    if L<=0:
        doc += "<p>あなたが現在取得している単位数は<b>{}</b>！卒業できます、おめでとう！！</p>".format(num)
    else:
        doc += "<p>あなたが現在取得している単位数は<b>{}</b>！卒業まであと<b>{}<b>単位必要です、頑張ろう！</p>".format(num,L)  
    # クローズ処理
    cur.close() 
    conn.close()
    doc += "</body></html>"
    return doc