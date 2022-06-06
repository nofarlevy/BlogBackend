from typing import List, Tuple, Union, Dict
import json


class Post:
    def __init__(self, post_id, title, content, user_id, date, img):
        self.post_id = post_id
        self.title = title
        self.content = content
        self.user_id = user_id
        self.date = date
        self.img = img

    def jsonify_post(self):
        return {
            "ID": self.id,
            "TITLE": self.title,
            "CONTENT": self.content,
            "USER_ID": self.user_id,
            "PUBLISHDAY": self.date,
            "IMG": self.img
        }


