from flask import (render_template, url_for, flash,
                   redirect, request, abort)
from flask_login import current_user, login_required
from app import db
from app.models.models import Post, Comment, Draft
from app.posts.forms import PostForm
from app.comment.form import CommentForm
from app.auth.utils import save_picture
from . import posts

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()   
    if request.method == 'POST':   
        if form.validate_on_submit():
            coverImage = save_picture(form.picture.data, 'cover_images')
            if form.draft.data:
                draft = Draft(title=form.title.data, description=form.description.data,   
                tag = form.tag.data, cover_image=coverImage, content=form.content.data, user=current_user)
                db.session.add(draft)
                db.session.commit()
                flash('Your draft has been created!', 'success')
            if form.submit.data:
                post = Post(title=form.title.data, description=form.description.data,  
                tag = form.tag.data, cover_image=coverImage, content=form.content.data, author=current_user)
                db.session.add(post)
                db.session.commit()
                flash('Your post has been created!', 'success')
                return redirect(url_for('main.home'))
    return render_template('public/create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>", methods=["GET","POST"])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if request.method == 'POST':  
        if form.validate_on_submit:
            if form.body.data != None:
                comment = Comment(body=form.body.data, post=post,
                                author=current_user)
                db.session.add(comment)
                db.session.commit()
                return redirect(url_for('posts.post',post_id=post.id))
    comments = Comment.query.filter_by(post=post)\
        .order_by(Comment.timestamp.desc())
    return render_template('public/post.html', title=post.title, post=post, comments=comments, form=form)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if request.method == 'POST':  
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash('Your post has been updated!', 'success')
            return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('public/create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete")
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

@posts.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)