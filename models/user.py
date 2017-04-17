import uuid
from src.models.blog import Blog
from src.common.database import Database
from flask import session


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one('users', query={'email': email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one(collection='users',
                                 query={'_id': _id})
        if data is not None:
            return cls(**data)
        pass

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            return user['password'] == password
        return False

    @classmethod
    def register(cls, email, password):
        if User.get_by_email(email=email) is None:
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            # User exists
            return False

    @staticmethod
    def login(user_email):
        # Login valid has already been checked.
        session['email'] = user_email

    @staticmethod
    def log_out():
        session['email']= None

    def get_blogs(self):
        Blog.get_by_author_id(self._id)

    def save_to_mongo(self):
        Database.insert(collection='users',
                        data=self.json())

    def new_blog(self, title, description):
        blog = Blog(author='email',
                    author_id=self._id,
                    title= title,
                    description=description)
        blog.save_to_mongo()

    def new_post(self, title, blog_id, content, date):
        blog = Blog.from_mongo(id= blog_id)
        blog.new_post(title=title,
                      content=content,
                      date=date)

    def json(self):
        return {
            'email': self.email,
            'password': self.password,
            '_id': self._id
        }
