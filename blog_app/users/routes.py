from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from blog_app import bcrypt, db
from blog_app.models import User
from blog_app.users.forms import UserLoginForm, UserRegistrationForm

users = Blueprint('users', __name__)


@users.route('/')
def index():
    return redirect('profile')


@users.route('profile/')
@login_required
def profile():
    return render_template('users/user_profile.html')


@users.route('register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.index'))

    form = UserRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password1.data).decode('utf-8')
        user = User(email=form.email.data,
                    username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created.', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/user_register.html', form=form)


@users.route('login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.index'))

    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('posts.index'))
        else:
            flash('You have entered wrong credentials.', 'danger')
    return render_template('users/user_login.html', form=form)


@users.route('logout/')
def logout():
    logout_user()
    return render_template('users/user_logout.html')
