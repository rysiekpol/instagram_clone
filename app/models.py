from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from hashlib import md5

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    photos = db.relationship('Photo', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    liked_photos = db.relationship('Photo', secondary='user_likes', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class UserLikes(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(140))
    description = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='photo', lazy='dynamic')

    def __repr__(self):
        return f'<Post {self.description}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(260))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Comment {self.comment}>'
