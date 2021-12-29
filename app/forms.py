from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, \
    SelectMultipleField, DateTimeField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email
from app.models import User, Question, Interview
from datetime import datetime


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    password = PasswordField('Password', validators=[DataRequired()])
    is_admin = BooleanField("Admin status", default=False)
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class QuestionForm(FlaskForm):

    question_field = TextAreaField("Question", validators=[DataRequired()])
    answer = StringField("Answer", validators=[DataRequired()])
    max_grade = IntegerField("Maximal Grade", validators=[DataRequired()], default=10)
    category = StringField("Category", validators=[DataRequired()])
    submit = SubmitField("Add")


class InterviewForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    applicant = StringField('Applicant', validators=[DataRequired()])
    questions_list = SelectMultipleField("Choose questions", choices=Question.create_list())
    users_list = SelectMultipleField("Choose interviewers", choices=User.create_list())
    date = DateTimeField("Chose date and time of interview in format d.m.Y H:M'", format='%d.%m.%Y %H:%M',
                         default=datetime.utcnow)
    submit = SubmitField("Submit")

    @classmethod
    def choice(cls):
        form = cls()
        form.questions_list.choices = Question.create_list()
        form.users_list.choices = User.create_list()
        return form


class GradeForm(FlaskForm):
    questions_list = SelectField("Choose Questions", choices=Question.create_list())
    users_list = SelectField("Choose Interviewers", choices=User.create_list())
    interviews = SelectField("Choose Interview", choices=Interview.create_list())
    submit = SubmitField('add')

    @classmethod
    def choice(cls):
        form = cls()
        form.users_list.choices = User.create_list()
        form.questions_list.choices = Question.create_list()
        form.interviews.choices = Interview.create_list()
        return form


class GradeQuestionForm(FlaskForm):
    grades_list = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]
    grade_field = SelectField("Give a grade to the answer", choices=grades_list)
    submit = SubmitField('Submit')
