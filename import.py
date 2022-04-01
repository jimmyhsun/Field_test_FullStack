import mysql.connector
import pandas as pd

connection = mysql.connector.connect(host="127.0.0.1", port="3306",
                                     database="one",
                                     user="root",
                                     password="8899",
                                     auth_plugin='mysql_native_password')
mycursor = connection.cursor()

df = pd.read_csv("dns_sample.csv")
datalist = df.values.tolist()
for i in datalist:
    command = ("insert into two  values(now(),'{:f}','None','{:s}','{:d}','{:s}','{:d}','{:s}')".format(i[0], i[1], i[2], i[3], i[4], i[5]))
    mycursor.execute(command)
    connection.commit()
