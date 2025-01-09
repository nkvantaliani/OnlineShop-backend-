from flask_login import UserMixin
from ext import db, login_manager

class BaseModel():
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()

class Product(db.Model, BaseModel):
    __tablename__ = "products"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    img = db.Column(db.String(), nullable=False, default="static/images/defult_img.jpg")

class User(db.Model, BaseModel,UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    post = db.relationship('Post')


@login_manager.user_loader
def load_user(user_id):
   return User.query.get(user_id)

class Post(db.Model, BaseModel):
    __tablename__ = "posts"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False )
    content = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)

