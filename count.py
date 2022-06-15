import sqlite3 
#from flask import Flask, render_template

dbname = 'credit.db'   #DBを指定

conn = sqlite3.connect(dbname) 

cur = conn.cursor() 

e=open('result.html','w')
e.write('<h1>知識情報・図書館学類システム主専攻の卒業単位の確認\n</h1>')
e.close()
        
#------------------------------------------------------------
#必修科目の判定
def decision(name,kamoku,need):
    number=0
    for row in cur.execute(kamoku):
        number+=row[0]
    if number<need:
        lack=need-number 
        f=open('result.html','a')
        f.write('<font color="red">{}の単位が{}単位足りていません。\n</font>'.format(name,lack))
        f.close()
    else:
        g=open('result.html','a')
        g.write('{}の単位は十分です。\n'.format(name))
        g.close()


#体育(2)
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
pronyu='SELECT 単位数 FROM sample WHERE 総合評価 in ("A+","A","B","C") and 科目番号 like "GE181%" or 科目番号 like "GE106%";'
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
for row in cur.execute(allcredit):
    num+=row[0]
    l=124-num
h=open('result.html','a')
if l<=0:
    h.write("<h3>あなたが現在取得している単位数は{}！卒業できます、おめでとう！！</h3>\n".format(num))
else:
    h.write("<h3>あなたが現在取得している単位数は{}！卒業まであと{}単位必要です、頑張ろう！</h3>\n".format(num,l))
h.close()

# クローズ処理
cur.close() 
conn.close()
