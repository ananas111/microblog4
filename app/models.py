from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login, admin
from flask_admin.contrib.sqla import ModelView

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean(False))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    question_field = db.Column(db.Text)
    answer = db.Column(db.String(64))
    max_grade = db.Column(db.Integer)
    category = db.Column(db.String(128))

    def __repr__(self):
        return f"{self.short_description}"


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Question, db.session))
