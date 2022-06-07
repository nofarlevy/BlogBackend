from flask import Blueprint, render_template, abort
from flask import Flask, request, jsonify
from consts import database_consts
from dal import sql_database
from services import twilio_service


actions = Blueprint('actions', __name__, url_prefix='/actions')


@actions.route("/add-like", methods=['GET'])
def add_like():
    try:
        post_id = request.args.get('post_id')
        user_id = request.args.get('user_id')
        data = f'{post_id},{user_id}'
        result = sql_database.insert_data("like", database_consts.COLOUM_TABLE_LIKE, data)
        return jsonify(result)
    except (ValueError, AttributeError) as e:
        return jsonify({'error': f'Could not query from database {e}'}), 400


@actions.route("/add-comment", methods=['POST'])
def add_comment():
    try:
        result = sql_database.add_comment(request.json)
        message = "Hey, you got a new comment :)"
        phone_n = sql_database.get_phone_of_post_author(request.json["POST_ID"])
        twilio_service.send_message(message, phone_n)
        return jsonify(result)
    except (ValueError, AttributeError) as e:
        return jsonify({'error': f'Could not query from database {e}'}), 400

