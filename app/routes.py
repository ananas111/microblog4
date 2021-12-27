from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, QuestionForm, InterviewForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Question, Interview, Grade
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
    interviews = Interview.query.all()
    return render_template('interview_list.html', username=username, interviews=interviews)


@app.route('/interview_list')
def interview_list():
    interviews = Interview.query.all()
    return render_template('interview_list.html', interviews=interviews)


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


@app.route('/create_interview', methods=["GET", "POST"])
def create_interview():
    if current_user.is_authenticated:
        form = InterviewForm().choice()
        if form.validate_on_submit():
            questions_list = []
            users_list = []
            for question_id in form.questions_list.data:
                question = Question.query.filter_by(id=question_id).first()
                questions_list.append(question)
            for user_id in form.users_list.data:
                user = User.query.filter_by(id=user_id).first()
                users_list.append(user)
            interview = Interview(applicant=form.applicant.data, questions_list=questions_list,
                                  users_list=users_list, date=form.date.data)
            interview_grade = [interview]
            for user in users_list:
                for question in questions_list:
                    grade = Grade(question=question, interviewer=user, interview=interview)
                    interview_grade.append(grade)
            db.session.add_all(interview_grade)
            db.session.commit()
            flash('Congratulations, you created an interview!')
            return redirect(url_for('interview_list'))
        return render_template('create_interview.html', form=form)
    else:
        flash('Error!')
        return render_template('index.html')

