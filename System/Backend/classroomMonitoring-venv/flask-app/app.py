import re
from flask import Flask,request,render_template,redirect
import flask
import MySQLdb
import json
import datetime


app = Flask(__name__)



''' connect to database'''
mydb = MySQLdb.connect(host = "ec2-54-162-123-217.compute-1.amazonaws.com", port = 3306, user="remoteuser", passwd = "yolo1234",database = "db")




@app.route('/test')
def test():
    cursor = mydb.cursor() 
    insertQuery = 'INSERT INTO examroom(ExamRoomID,examID,SchoolName) VALUES (%s, %s, %s)'
    cursor.execute(insertQuery, ('72', 'CSCE2201','AUC', ))
    mydb.commit()
    cursor.close()
    return "Hello World"
if __name__ == "__main__":
    app.run(debug=True)
