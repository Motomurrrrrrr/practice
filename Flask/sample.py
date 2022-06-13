import os
import sqlite3
from flask import Flask, request, escape, render_template
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
    return rows

@app.route("/result")
def result():
    return render_template("result.html")