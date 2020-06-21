from flask import render_template, request
from app.models.models import Post
from app import cache
from . import main


@main.route("/")
@main.route("/home")
@cache.cached(300, key_prefix='home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('public/home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')