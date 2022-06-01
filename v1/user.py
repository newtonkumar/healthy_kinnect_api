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
            sqlQuery = "SELECT * FROM auth_user auth_u INNER JOIN accounts acc ON acc.user_id=auth_u.id"
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

    # Get the particular user details by passing id
    def get(user_id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "SELECT * FROM auth_user auth_u INNER JOIN accounts acc ON acc.user_id=auth_u.id WHERE id=%s"
            cursor.execute(sqlQuery, user_id)
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
    def delete(user_id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            sqlQuery = "DELETE FROM auth_user WHERE id=%s"
            cursor.execute(sqlQuery, (user_id))
            conn.commit()

            return jsonify(
                message="User has been deleted successfully",
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
