from math import trunc
import pymysql
from pymysql import cursors
from app import app
from settings.config import mysql
from flask import jsonify
from flask import flash, request
from datetime import datetime


class user:
    # To insert new student records
    def register():
        try:
            _json = request.json
            _first_name = _json['first_name']
            _last_name = _json['last_name']
            _username = _json['username']
            _password = _json['password']
            _conf_password = _json['conf_password']
            _email = _json['email']
            _mobile_no = _json['mobile_no']
            _age = _json['age']
            _address = _json['address']
            _location = _json['location']
            _hobbies = _json['hobbies']
            _workout_preferences = _json['workout_preferences']
            _dietary_preferences = _json['dietary_preferences']
            _gender = _json['gender']

            conn = mysql.connect()
            cursor = conn.cursor()
            # Insert into auth_user and get user_id
            userQuery = "START TRANSACTION;" \
                        "INSERT INTO auth_user (first_name, last_name, email, password, is_superuser, username, " \
                        "is_staff, is_active)" \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);" \
                        "SELECT LAST_INSERT_ID() AS user_id; " \
                        "COMMIT;"
            user_data = (_first_name, _last_name, _email, _password, False, _username, False, True)
            cursor.execute(userQuery, user_data)
            result = cursor.fetchone()

            _user_id = result['user_id']

            # insert into accounts table
            sqlQuery = "INSERT INTO accounts(mobile_no, age, address, hobbies, workout_preferences, " \
                       "dietary_preferences, gender, location, user_id) " \
                       "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            account_data = (_mobile_no, _age, _address, _hobbies, _workout_preferences, _dietary_preferences,
                            _gender, _location, _user_id)
            cursor.execute(sqlQuery, account_data)
            conn.commit()

            return jsonify(
                message='User has been registered successfully.',
                status=200
            )
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    # To list down all students
    def list():
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            # Get records from database table
            sqlQuery = "SELECT * FROM students"
            cursor.execute(sqlQuery)
            rows = cursor.fetchall()
            conn.commit()

            return jsonify(
                data=rows,
                status=200
            )
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    # To update student details
    def update():
        try:
            _json = request.json
            _student_id = _json['id']
            _roll_no = _json['roll_no']
            _first_name = _json['first_name']
            _last_name = _json['last_name']
            _class = _json['class']
            _age = _json['age']
            _address = _json['address']
            _phone = _json['phone']
            _whatsapp = _json['whatsapp']
            _status = _json['status']
            _modified_at = datetime.now()

            if _student_id and request.method == 'PUT':
                # Update query for student records
                sqlQuery = "UPDATE students SET roll_no=%s, first_name=%s, last_name=%s, class=%s, age=%s, address=%s, phone=%s, whatsapp=%s, status=%s, modified_at=%s WHERE id=%s"
                data = (
                    _roll_no, _first_name, _last_name, _class, _age, _address, _phone, _whatsapp, _status, _modified_at,
                    _student_id)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sqlQuery, data)
                conn.commit()

                return jsonify(
                    message='Student details updated successfully',
                    status=200
                )
            else:
                return student.not_found()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    # Get the particular student details by passing id
    def get(student_id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "SELECT * FROM students WHERE id=%s"
            cursor.execute(sqlQuery, student_id)
            row = cursor.fetchone()

            return jsonify(
                data=row,
                status=200
            )
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    # Delete student record
    def delete(student_id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            sqlQuery = "DELETE FROM students WHERE id=%s"
            cursor.execute(sqlQuery, (student_id))
            conn.commit()

            return jsonify(
                message="Student deleted successfully",
                status=200
            )
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    @app.errorhandler(404)
    def not_found(error=None):
        message = {
            'status': 404,
            'message': 'There is no record: ' + request.url,
        }
        res = jsonify(message)
        res.status_code = 404

        return res

    if __name__ == "__main__":
        app.run(debug=True)
