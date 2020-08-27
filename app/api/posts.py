from flask import jsonify, request, url_for, g, abort
from app import db
from app.models.models import Post,Comment
from app.api import api
from app.api.auth import token_auth
from app.api.errors import bad_request


@api.route('/posts/<int:id>', methods=['GET'])
@token_auth.login_required
def get_post(id):
    return jsonify(Post.query.get_or_404(id).to_dict())


@api.route('/posts', methods=['GET'])
@token_auth.login_required
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Post.to_collection_dict(Post.query, page, per_page, 'api.get_posts')
    return jsonify(data)


@api.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json() or {}
    if 'title' not in data or 'description' not in data or 'tag' not in data or 'content' not in data or 'cover_image' not in data:
        return bad_request('must include title, description, tag, content and cover_image fields')
    post = Post()
    post.from_dict(data)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    response = jsonify(post.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_post', id=post.id)
    return response


@api.route('/posts/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_post(id):
    if g.current_user.id != id:
        abort(403)
    post = Post.query.get_or_404(id)
    data = request.get_json() or {}
    user.from_dict(data)
    db.session.commit()
    return jsonify(user.to_dict())

@api.route('/posts/<int:id>/comments', methods=['GET'])
@token_auth.login_required
def get_post_comments(id):
    post = Post.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Post.to_collection_dict(post.comments, page, per_page,
                                   'api.get_followers', id=id)
    return jsonify(data)

@api.route('/posts/<int:id>/comments', methods=['Post'])
@token_auth.login_required
def comment_on_post(id):
    post = Post.query.get_or_404(id)
    data = request.get_json() or {}
    if 'body' not in data:
        return bad_request('must include body field')
    comment = Comment()
    comment.post = post
    comment.author = g.current_user
    db.session.add(post)
    db.session.commit()
    response = jsonify(post.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_post', id=post.id)
    return response


