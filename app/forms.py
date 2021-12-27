from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email
from app.models import User


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

