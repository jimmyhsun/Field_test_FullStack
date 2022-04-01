from flask import Flask, render_template,request
import mysql.connector

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/search', methods=['POST','GET'])
def search():
    return render_template('search.html')


@app.route('/search2', methods=['POST','GET'])
def search2():
    if request.method == "POST":
        connection = mysql.connector.connect(host="127.0.0.1", port="3306",
                                             database="one",
                                             user="root",
                                             password="8899",
                                             auth_plugin='mysql_native_password')
        mycursor = connection.cursor()
        sourceip = request.form.get('sourceip')
        FQDN = request.form.get('fqdn')
        if FQDN == "":
            command = ("select * from two where SourceIP='{:s}'".format(sourceip))
            mycursor.execute(command)
            result = mycursor.fetchall()
            return render_template("result.html",result=result)
        elif sourceip == "":
            command = ("select * from two where DNS A record query='{:s}'".format(FQDN))
            mycursor.execute(command)
            result = mycursor.fetchall()
            return render_template("result.html", result=result)
        else:
            command = ("select * from two where DNS A record query='{:s}'&SourceIP='{:s}'".format(FQDN,sourceip))
            mycursor.execute(command)
            result = mycursor.fetchall()
            return render_template("result.html", result=result)

if __name__ == '__main__':
    app.debug = True
    app.run()