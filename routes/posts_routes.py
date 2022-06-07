from flask import Blueprint, render_template, abort
import psycopg2
from flask import Flask, request, jsonify
from consts import database_consts
from dal import sql_database


posts = Blueprint('posts', __name__, url_prefix='/posts')


@posts.route("/post-comments", methods=['GET'])
def get_post_comment():
    post_id = request.args.get('post_id')
    return jsonify(sql_database.comment_by_post(post_id))


@posts.route("/get-posts", methods=['GET', 'POST'])
def get_posts():
    try:
        result = sql_database.get_posts_from_database()
        return jsonify(result)
    except psycopg2.DatabaseError as error:
        return error


@posts.route("/get-posts-by-user-id", methods=['GET'])
def get_posts_by_user_id():
    user_id = request.args.get('userid')
    return jsonify(sql_database.get_posts_by_user_id(user_id))


@posts.route("/get-posts-by-date", methods=['GET'])
def get_posts_by_date():
    date = request.args.get('date')
    return jsonify(sql_database.query_by_date(date))


@posts.route("/search-post", methods=['GET'])
def get_posts_by_search():
    data = request.args.get('data')
    return jsonify(sql_database.search_data_in_posts(data))


@posts.route("/post-likes", methods=['GET'])
def get_post_likes():
    post_id = request.args.get('post_id')
    return jsonify(sql_database.likes_by_post(post_id))


@posts.route("/post-comments", methods=['GET'])
def get_post_comment():
    post_id = request.args.get('post_id')
    return jsonify(sql_database.comment_by_post(post_id))


@posts.route("/insert-posts", methods=['POST'])
def insert_posts():
    try:
        result = sql_database.insert_data("posts", database_consts.COLOUM_TABLE_POST, request.json)
        return jsonify(result)
    except (ValueError, AttributeError) as e:
        return jsonify({'error': f'Could not query from database {e}'}), 400


@posts.route("/get-phone-by-post", methods=['GET'])
def get_phone_by_postid():
    post_id = request.args.get('post_id')
    phone_dict = {"phone": jsonify(sql_database.get_phone_of_post_author(post_id))}
    return phone_dict


@posts.route("/edit-post", methods=['POST'])
def edit_post():
    try:
        result = sql_database.edit_post(request.json)
        return jsonify(result)
    except (ValueError, AttributeError) as e:
        return jsonify({'error': f'Could not query from database {e}'}), 400
