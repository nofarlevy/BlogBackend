from typing import List, Tuple, Union, Dict
import json


class User:
    def __init__(self, id, name, phone, email):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email

    def jsonify_user(self):
        return {
            "USER_ID": self.id,
            "NAME": self.name,
            "PHONE": self.phone,
            "EMAIL": self.email
        }

    @staticmethod
    def jsonify_list_of_user(users_list: List['User']):
        result = []
        for user in users_list:
            result.append(user.jsonify_user())
        return result

    @staticmethod
    def from_database_user(json: Dict[str, Union[str, int]]):
        return User(json["USER_ID"], json["NAME"], json["PHONE"], json["EMAIL"])

    @staticmethod
    def from_data_user_list(json: Dict[str, Union[str, int]]):
        user_list = []
        for user in json:
            user_list.append(User.from_database_user(user))
        return user_list


