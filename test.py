import mysql.connector as connector

con = connector.connect(host='localhost', user='root', password='', database='healthy_kinnect')
print(con)

from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello world! Test'

from dotenv import load_dotenv

print('111')