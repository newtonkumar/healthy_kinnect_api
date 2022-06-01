import pymysql
from app import app
from settings.config import mysql


class DBHelper:
    def __init__(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlQuery = 'CREATE TABLE IF NOT EXISTS accounts' \
                   '(id int primary key NOT NULL AUTO_INCREMENT,' \
                   'mobile_no BIGINT(20) NOT NULL, ' \
                   'age INT(11) NOT NULL, ' \
                   'address TEXT NOT NULL, ' \
                   'hobbies VARCHAR(255) NOT NULL, ' \
                   'workout_preferences TEXT NOT NULL, ' \
                   'dietary_preferences TEXT NOT NULL, ' \
                   'gender VARCHAR(6) NOT NULL, ' \
                   'user_id INT, CONSTRAINT fk_auth_user FOREIGN KEY(user_id) REFERENCES auth_user(id)' \
                   'ON UPDATE CASCADE ON DELETE CASCADE' \
                   'location TEXT NULL) ENGINE=INNODB'
        cursor.execute(sqlQuery)
        print('Student Table Created!\n')
