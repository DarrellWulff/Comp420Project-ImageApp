from enum import unique
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql import expression
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Image(db.Model):
    image_id = db.Column(db.Integer, primary_key=true)
    img = db.Column(db.LargeBinary(length=(2**32)-1))
    image_name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def get_id(self):
        return self.image_id

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    post_note = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    image_id = db.Column(db.Integer, db.ForeignKey('image.image_id'))
    

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    is_active = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
    posts = db.relationship('Post')

    def get_id(self):
        return self.user_id
