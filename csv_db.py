import sqlite3
import pandas as pd

df = pd.read_csv("submit.csv")

df.culums=['学籍番号','学生氏名','科目番号','科目名','単位数','春学期','秋学期','総合評価','科目区分','開講年度','開講区分']
dbname='mysample.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()
df.to_sql('sample', conn, if_exists='replace')
select_sql = 'SELECT * FROM sample'
for row in cur.execute(select_sql):
    print(row)
cur.close()
conn.close()
