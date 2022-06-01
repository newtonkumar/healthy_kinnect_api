import pymysql
from app import app
from v1.user import user
from settings.config import mysql
from flask import jsonify
from flask import flash, request


# Version-1 API
@app.route('/v1/user/register', methods=['POST'])
def register_user():
    return user.register()


@app.route('/v1/user/list', methods=['GET'])
def list_user():
    return user.list()


@app.route('/v1/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return user.get(user_id)


@app.route('/v1/user/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return user.delete(user_id)


if __name__ == "__main__":
    app.run(debug=True)
