from flask import Blueprint, render_template, abort
import psycopg2
from flask import Flask, request, jsonify
from model.user import User
from dal import sql_database


users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/get-list-userobj', methods=['GET', 'POST'])
def get_user_object():
    result = User.jsonify_list_of_user(User.from_data_user_list(request.json))
    return jsonify(result)


@users.route("/get-users", methods=['GET', 'POST'])
def get_users():
    try:
        result = sql_database.get_users_from_database()
        return jsonify(result)
    except psycopg2.DatabaseError as error:
        return error
