import pymysql
from app import app
from v1.user import user
from settings.config import mysql
from flask import jsonify
from flask import flash, request

#Version-1 API
@app.route('/v1/user/register', methods = ['POST'])
def register_user():
    return user.register()

@app.route('/v1/user/list', methods = ['GET'])
def list_user():
    return user.list()

@app.route('/v1/student/update', methods = ['PUT'])
def update_student():
    return student.update()

@app.route('/v1/student/<int:student_id>', methods = ['GET'])
def get_student(student_id):
    return student.get(student_id)

@app.route('/v1/student/delete/<int:student_id>', methods = ['DELETE'])
def delete_student(student_id):
    return student.delete(student_id)

#API : About Page
@app.route('/v1/about/details', methods = ['GET'])
def details():
    return about.details()



if __name__ == "__main__":
    app.run(debug=True)