from flask import jsonify, request, url_for, g, abort
from app import db
from app.models.models import User, Post
from app.api import api
from app.api.auth import token_auth
from app.api.errors import bad_request


@api.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@api.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)

@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    print(request.get_json())
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@api.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if g.current_user.id != id:
        abort(403)
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())
@api.route('/users/<int:id>/followers', methods=['GET'])
@token_auth.login_required
def get_followers(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.followers, page, per_page,
                                   'api.get_followers', id=id)
    return jsonify(data)


@api.route('/users/<int:id>/followed', methods=['GET'])
@token_auth.login_required
def get_followed(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.followed, page, per_page,
                                   'api.get_followed', id=id)
    return jsonify(data)

@api.route('/users/follow/<int:id>', methods=['POST'])
@token_auth.login_required
def follow(id):
    user = User.query.get(id)
    if user is None:
        return bad_request('user is not found')
    if user == g.current_user:
        return bad_request('You cannot follow yourself!')
    g.current_user.follow(user)
    db.session.commit()
    response = jsonify({"message":f"you are now following {user.username}"})
    response.status_code = 200
    return response


@api.route('/users/unfollow/<int:id>', methods=['POST'])
@token_auth.login_required
def unfollow(id):
    user = User.query.get(id)
    if user is None:
        return bad_request('user is not found')
    if user == g.current_user:
        return bad_request('You cannot unfollow yourself!')
    g.current_user.unfollow(user)
    db.session.commit()
    response = jsonify({"message":f"you have unfollowed {user.username}"})
    response.status_code = 200
    return response


@api.route('/user/like_post/<int:post_id>', methods=['POST'])
@token_auth.login_required
def like_post(post_id):
    post = Post.query.get(post_id)
    if g.current_user.has_liked_post(post):
        return bad_request('you have already liked this post')
    g.current_user.like_post(post)
    db.session.commit()
    response = jsonify({"message":f"you have liked post {post.id}"})
    response.status_code = 200
    return response

@api.route('/user/unlike_post/<int:post_id>', methods=['POST'])
@token_auth.login_required
def unlike_post(post_id):
    post = Post.query.get(post_id)
    if not g.current_user.has_liked_post(post):
        return bad_request('you can\'t unlike this post because you have not liked this post yet')
    g.current_user.unlike_post(post)
    db.session.commit()
    response = jsonify({"message":f"you have unliked post {post.id}"})
    response.status_code = 200
    return response