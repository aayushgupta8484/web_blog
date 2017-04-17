import uuid
from post import Post
import datetime
from src.common.database import Database


class Blog(object):

    def __init__(self, author, author_id, title, description, _id=None):

        self.author = author
        self.author_id = author_id
        self.title = title
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self, title, content, date= datetime.datetime.utcnow()):
        post = Post(author=self.author,
                    title=title,
                    content=content,
                    blog_id=self._id,
                    created_date=date)
        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blogs_1', data=self.json())

    def json(self):
        return {
            'author': self.author,
            'author_id': self.author_id,
            'title': self.title,
            'description': self.description,
            '_id': self._id,
        }

    @classmethod
    def from_mongo(cls, id):
        inter = Database.find_one(collection='blogs_1', query={'_id': id})
        return cls(**inter)

    @classmethod
    def get_by_author_id(cls, author_id):
        data = Database.find(collection='blogs_1',
                      query={'author_id': author_id})
        return [cls(**blog) for blog in data]
