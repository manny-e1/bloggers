from flask import render_template, request, url_for
from app.models.models import Post
from flask_login import current_user
from . import main
from sqlalchemy import func


def most_liked():
	###############algorithm for poplar post by the num of likes##########
	# post = Post.query.all()
	# likes, iD, popular_post =[], [], []
	# for p in post:
	# 	likes.append(f'{p.likes.count()}:{p.id}')
	# likes = sorted(likes)[::-1][:5]
	# for ids in likes:
	# 	if ":" in ids:
	# 		iD.append(int(ids[ids.index(":")+1:]))
	# for i in iD:
	# 	pst = Post.query.get(i)
	# 	popular_post.append(pst)
	#######################################################################
	return Post().likes_count()

def catagory_query_count(string):
	return Post.query.filter_by(tag=string).count()
def catagory_query(string):
	page = request.args.get('page',1,type=int)
	return Post.query.filter_by(tag=string).paginate(page=page, per_page=5)

def catagory():
	software = catagory_query_count("Software")
	food = catagory_query_count("Food")
	lifestyle = catagory_query_count("Life Style")
	technology = catagory_query_count("Technology")
	
	return {"software":software,"food":food,"life_Style":lifestyle,"technology":technology}


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    randpost = Post.query.order_by(func.random()).paginate(page=page, per_page=5)
    return render_template('public/home.html', posts=posts, popular=most_liked(), random = randpost,
     catagory = catagory())

@main.route("/followed_post")
def followed_post():
	page = request.args.get('page', 1, type=int)
	posts = current_user.followed_posts().paginate(page=page, per_page=5)
	return render_template('public/home_followed.html', posts = posts,popular=most_liked(), catagory = catagory())

@main.route("/posts/tag/<tag>")
def tag(tag):
	if tag == "Life_style":
		tag = "Life Style"
	posts = catagory_query(tag)
	return render_template("public/tag.html",posts=posts,popular=most_liked(), catagory = catagory())
