from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, QuestionForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Question
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html", title='Home Page')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin')
def admin():
    return redirect('/home/admin')


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, first_name=form.first_name.data,
                    last_name=form.last_name.data, is_admin=form.is_admin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you registered a new user!')
        return redirect(url_for('users_list'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/create-question', methods=["GET", "POST"])
@login_required
def create_question():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(question_field=form.question_field.data,
                            answer=form.answer.data,
                            max_grade=form.max_grade.data,
                            category=form.category.data
                            )
        db.session.add(question)
        db.session.commit()
        flash('Congratulations, you added a new question!')
        return redirect(url_for('questions_list'))
    return render_template('create_question.html', form=form)


@app.route('/questions_list')
def questions_list():
    questions = Question.query.all()
    return render_template('questions_list.html', questions=questions)


@app.route('/users_list')
def users_list():
    users = User.query.all()
    return render_template('users_list.html', users=users)