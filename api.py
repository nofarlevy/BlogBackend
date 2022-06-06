import psycopg2
from flask import Flask, request, jsonify
import requests
from model.user import User
from consts import database_consts
from dal import sql_database
import time
from services import twilio_service

api = Flask(__name__)
api_key = "9e70d3c23540669ff1c632376b427228"
base_url = "http://api.openweathermap.org/data/2.5/weather?"


@api.route('/')
def hello():
    return 'Welcome'


@api.route('/api/get-list-userobj', methods=['GET', 'POST'])
def get_user_object():
    result = User.jsonify_list_of_user(User.from_data_user_list(request.json))
    return jsonify(result)


# @api.route("/api/get-users", methods=['GET', 'POST'])
# def get_posts():
#     return jsonify(sql_database.get_posts())

@api.route("/api/get-posts", methods=['GET', 'POST'])
def get_posts():
    try:
        result = sql_database.get_posts_from_database()
        return jsonify(result)
    except psycopg2.DatabaseError as error:
        return error


@api.route("/api/get-users", methods=['GET', 'POST'])
def get_users():
    try:
        result = sql_database.get_users_from_database()
        return jsonify(result)
    except psycopg2.DatabaseError as error:
        return error


@api.route("/api/meta-data", methods=['GET', 'POST'])
def meta_data():
    named_tuple = time.localtime()
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)

    print("" + time_string)


@api.route("/api/get-posts-by-user-id", methods=['GET'])
def get_posts_by_user_id():
    user_id = request.args.get('userid')
    return jsonify(sql_database.get_posts_by_user_id(user_id))


@api.route("/api/get-posts-by-date", methods=['GET'])
def get_posts_by_date():
    date = request.args.get('date')
    return jsonify(sql_database.query_by_date(date))


@api.route("/api/get-phone-by-post", methods=['GET'])
def get_phone_by_postid():
    post_id = request.args.get('post_id')
    phone_dict = {"phone": jsonify(sql_database.get_phone_of_post_author(post_id))}
    return phone_dict


@api.route("/api/search-post", methods=['GET'])
def get_posts_by_search():
    data = request.args.get('data')
    return jsonify(sql_database.search_data_in_posts(data))


@api.route("/api/post-likes", methods=['GET'])
def get_post_likes():
    post_id = request.args.get('post_id')
    return jsonify(sql_database.likes_by_post(post_id))


@api.route("/api/post-comments", methods=['GET'])
def get_post_comment():
    post_id = request.args.get('post_id')
    return jsonify(sql_database.comment_by_post(post_id))


@api.route("/api/insert-posts", methods=['POST'])
def insert_posts():
    try:
        result = sql_database.insert_data("posts", database_consts.COLOUM_TABLE_POST, request.json)
        return jsonify(result)
    except (ValueError, AttributeError) as e:
        return jsonify({'error': f'Could not query from database {e}'}), 400


@api.route("/api/add-like", methods=['GET'])
def add_like():
    try:
        post_id = request.args.get('post_id')
        user_id = request.args.get('user_id')
        data = f'{post_id},{user_id}'
        result = sql_database.insert_data("like", database_consts.COLOUM_TABLE_LIKE, data)
        return jsonify(result)
    except (ValueError, AttributeError) as e:
        return jsonify({'error': f'Could not query from database {e}'}), 400


@api.route("/api/add-comment", methods=['POST'])
def add_comment():
    try:
        result = sql_database.add_comment(request.json)
        message = "Hey, you got a new comment :)"
        phone_n = sql_database.get_phone_of_post_author(request.json["POST_ID"])
        twilio_service.send_message(message,phone_n)
        return jsonify(result)
    except (ValueError, AttributeError) as e:
        return jsonify({'error': f'Could not query from database {e}'}), 400


@api.route("/api/edit-post", methods=['POST'])
def edit_post():
    try:
        result = sql_database.edit_post(request.json)
        return jsonify(result)
    except (ValueError, AttributeError) as e:
        return jsonify({'error': f'Could not query from database {e}'}), 400


if __name__ == '__main__':
    api.run(port=8080)
