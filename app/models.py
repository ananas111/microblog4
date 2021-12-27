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
    __tablename__ = "users"
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
        return f"{self.question_field}"


interview_user = db.Table('interview_user',
                          db.Column('users_id', db.ForeignKey('users.id'), primary_key=True),
                          db.Column('interview_id', db.ForeignKey('interviews.id'), primary_key=True)
                          )

interview_question = db.Table('interview_question',
                              db.Column('question_id', db.ForeignKey('questions.id'), primary_key=True),
                              db.Column('interview_id', db.ForeignKey('interviews.id'), primary_key=True)
                              )


class Interview(db.Model):
    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True)
    applicant = db.Column(db.String)
    questions_list = db.relationship('Question', secondary=interview_question, lazy='subquery',
                                     backref=db.backref('interviews', lazy=True))
    users_list = db.relationship('User', secondary=interview_user, lazy='subquery',
                                 backref=db.backref('interviews', lazy=True))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.applicant}"


class Grade(db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    question = db.relationship("Question", backref="grades")
    interviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    interviewer = db.relationship("User", backref="grades")
    interview_id = db.Column(db.Integer, db.ForeignKey('interviews.id'))
    interview = db.relationship("Interview", backref="grades")
    grade = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"{self.interviewer} gives {self.applicant} {self.grade} for question {self.question}"


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Question, db.session))
admin.add_view(ModelView(Interview, db.session))
admin.add_view(ModelView(Grade, db.session))
