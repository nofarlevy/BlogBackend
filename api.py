from flask import Flask, request, jsonify
import time
from routes import posts_routes, users_routers, actions_routers

api = Flask(__name__)
api.register_blueprint(posts_routes.posts)
api.register_blueprint(users_routers.users)
api.register_blueprint(actions_routers.actions)
api_key = "9e70d3c23540669ff1c632376b427228"
base_url = "http://api.openweathermap.org/data/2.5/weather?"


@api.route('/')
def hello():
    return 'Welcome to my blog'


@api.route("/api/meta-data", methods=['GET', 'POST'])
def meta_data():
    named_tuple = time.localtime()
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)

    print("" + time_string)


if __name__ == '__main__':
    api.run(port=8080)
