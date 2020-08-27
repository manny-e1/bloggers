from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from werkzeug.urls import url_parse
from app.auth.forms import LoginForm, RegistrationForm, UpdateAccountForm
from app.models.models import User, Post
from app.auth.utils import save_picture
import os
from app.auth.emails import send_email, send_change_email
from . import users



@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if request.method == 'POST':  
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password','danger')
                return redirect(url_for('users.login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.home')
            return redirect(next_page)
    return render_template('public/auth/login.html',  form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if request.method == 'POST':  
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            send_email(user, "confirmation")
            flash('A confirmation email has been sent to you by email.','info')
            return redirect(url_for('users.login'))
    return render_template('public/auth/register.html', form=form)


@users.route('/confirm/<token>')
@login_required
def confirm_mail(token):
    if current_user.confirmed:
        return redirect(url_for('main.home'))
    if current_user.confirm_email(token):
        flash('You have confirmed your account. Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired.','danger')
    return redirect(url_for('main.home'))



@users.before_app_request
def before_request():
    if current_user.is_authenticated:
        if not current_user.confirmed and request.endpoint[:5]!='users':
            return redirect(url_for('users.unconfirmed'))


@users.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.home'))
    return render_template('public/auth/unconfirmed.html')

@users.route('/confirm')
@login_required
def resend_confirmation():
    send_email(current_user)
    flash('A new confirmation email has been sent to you by email.', 'info')
    return redirect(url_for('main.home'))

@users.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.','info')
    else:
        flash('Invalid request.','error')
    return redirect(url_for('users.account'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if request.method == 'POST':  
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data,'profile_pics')
                current_user.image_file = picture_file
            current_user.username = form.username.data
            if form.username.data != current_user.username:
                current_user.username = form.username.data
                flash('Your username has been updated','info')
            if form.email.data != current_user.email:    
                newemail = form.email.data.lower()
                # send_change_email(user=current_user, email=newemail)
                current_user.email = newemail
                flash('A confirmation email has been sent to you by email.','info')
            db.session.commit()
            return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('public/account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('public/user_posts.html', posts=posts, user=user)


@users.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username),'error')
        return redirect(url_for('main.home'))
    if user == current_user:
        flash('You cannot follow yourself!','warning')
        return redirect(url_for('users.user_posts', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username),'info')
    return redirect(url_for('users.user_posts', username=username))

@users.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username),'error')
        return redirect(url_for('main.home'))
    if user == current_user:
        flash('You cannot unfollow yourself!','warning')
        return redirect(url_for('users.user_posts', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username),'warning')
    return redirect(url_for('users.user_posts', username=username))