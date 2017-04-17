
from src.common.database import Database
import uuid
import datetime


class Post(object):

    def __init__(self, author, title, blog_id, content, created_date=datetime.datetime.utcnow(), _id=None):
        self.author = author
        self.title = title
        self.content = content
        self.blog_id = blog_id
        self._id = uuid.uuid4().hex if _id is None else _id
        self.created_date = created_date

    def save_to_mongo(self):
        Database.insert(collection='posts_1', data=self.json())

    def json(self):
        return {
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "blog_id":self.blog_id,
            "_id": self._id,
            "created_date": self.created_date
        }

    @classmethod
    def from_mongo(cls, id):
        post_data = Database.find_one(collection='posts_1', query={'_id': id})
        return cls(**post_data)


    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(collection='posts_1', query={'blog_id':id})]




