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
            _is_superuser = _json['is_superuser']
            _is_staff = _json['is_staff']
            _is_active = _json['is_active']

            conn = mysql.connect()
            cursor = conn.cursor()
            # Insert into auth_user and get user_id
            userQuery = "BEGIN;" \
                        "INSERT INTO auth_user (first_name, last_name, email, password, is_superuser, username, " \
                        "is_staff, is_active)" \
                        "VALUES(%s, %s, %s, %s, %s, %s, %s, %s);" \
                        "INSERT INTO accounts(mobile_no, age, address, hobbies, workout_preferences, " \
                        "dietary_preferences, gender, location, user_id) " \
                        "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, LAST_INSERT_ID());COMMIT;"
            user_data = (_first_name, _last_name, _email, _password, _is_superuser, _username, _is_staff, _is_active,
                         _mobile_no, _age, _address, _hobbies, _workout_preferences, _dietary_preferences,
                         _gender, _location)
            cursor.execute(userQuery, user_data)

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
            sqlQuery = "SELECT " \
                       "auth_u.id, auth_u.username, auth_u.first_name, auth_u.last_name, auth_u.email, " \
                       "auth_u.is_active, " \
                       "acc.mobile_no, acc.age, acc.address, acc.hobbies, acc.workout_preferences, " \
                       "acc.dietary_preferences, " \
                       "acc.gender, acc.location " \
                       "FROM auth_user auth_u INNER JOIN accounts acc ON acc.user_id=auth_u.id"
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
            sqlQuery = "SELECT " \
                       "auth_u.id, auth_u.username, auth_u.first_name, auth_u.last_name, auth_u.email, " \
                       "auth_u.is_active, " \
                       "acc.mobile_no, acc.age, acc.address, acc.hobbies, acc.workout_preferences, " \
                       "acc.dietary_preferences, " \
                       "acc.gender, acc.location " \
                       "FROM auth_user auth_u " \
                       "INNER JOIN accounts acc ON acc.user_id=auth_u.id " \
                       "WHERE " \
                       "auth_u.id=%s"
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
            sqlQuery = "START TRANSACTION;" \
                       "DELETE FROM accounts WHERE user_id=%s;" \
                       "DELETE FROM auth_user WHERE id=%s;" \
                       "COMMIT;"
            cursor.execute(sqlQuery, (user_id, user_id))
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
