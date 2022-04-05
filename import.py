from flask import Flask, render_template,request
import sqlite3 as sql
import sqlite3
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/search', methods=['POST','GET'])
def search():
    return render_template('search.html')

@app.route('/csv_import', methods=['POST','GET'])
def csv_import():
    try:
        conn = sqlite3.connect('database.db')
        print("Opened database successfully")
        #創建TABLE
        conn.execute('CREATE TABLE date_one (DATE TEXT, Time TEXT, usec TEXT, SourceIP TEXT, SourcePort TEXT, DestinationIP TEXT, DestinationPort TEXT ,DNS A record query TEXT )')
        print("Table created successfully")
        conn.close()
        #讀取CSV
        df = pd.read_csv("dns_sample.csv")
        datalist = df.values.tolist()
        #INSERT to TaBLE
        with sql.connect("database.db") as con:
            cur = con.cursor()
            for i in datalist:
                cur.execute("INSERT INTO date_one  VALUES (date('now'),?,'None',?,?,?,?,?)",
                            (i[0], i[1], i[2], i[3], i[4], i[5]))
                con.commit()
        appoint = "匯入完成"
        return render_template("csv_import.html",appoint=appoint)
    except:
        appoint = "匯入失敗,已匯入過"
        return render_template("csv_import.html",appoint=appoint)

@app.route('/all_search', methods=['POST','GET'])
def all_search():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from date_one ")
    result = cur.fetchall()
    return render_template("result.html",result=result)


@app.route('/search2', methods=['POST','GET'])
def search2():
    if request.method == "POST":
        sourceip = request.form.get('sourceip')
        fqdn = request.form.get("fqdn")
        if fqdn == "":
            con = sql.connect("database.db")
            con.row_factory = sql.Row

            cur = con.cursor()
            cur.execute("select * from date_one where SourceIP=(?)",(sourceip,))
            result = cur.fetchall()
            return render_template("result.html",result=result)
        if sourceip == "":
            con = sql.connect("database.db")
            con.row_factory = sql.Row

            cur = con.cursor()
            cur.execute("select * from date_one where DNS A record query=(?)",(fqdn,))
            result = cur.fetchall()
            return render_template("result.html",result=result)
        else:
            con = sql.connect("database.db")
            con.row_factory = sql.Row

            cur = con.cursor()
            cur.execute("select * from date_one where DNS A record query=(?) & SourceIP=(?)", (fqdn,sourceip))
            result = cur.fetchall()
            return render_template("result.html", result=result)

@app.route('/init')
def init():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute(
        'CREATE TABLE date_one (DATE TEXT, Time TEXT, usec TEXT, SourceIP TEXT, SourcePort TEXT, DestinationIP TEXT, DestinationPort TEXT ,DNS A record query TEXT )')
    print("Table created successfully")
    conn.close()
    return None


if __name__ == '__main__':
    app.debug = True
    app.run()