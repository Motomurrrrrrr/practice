from doctest import run_docstring_examples
from flask import Flask
from flask import render_template

app = Flask(__name__)

#HTMLはpathから取得して表示させる(テンプレート)

@app.route("/") #ここを改変して機能を実装していく
def hello():
    return render_template("send.html") #templatesディレクトリから指定のを持ってくる

@app.route("/japan/<city>") #ここを改変して機能を実装していく
def japan(city):
    return render_template("hello.html", city=city) #html側の変数cityにcityを代入という意味

@app.route("/result")
def result():
    return render_template("result.html")