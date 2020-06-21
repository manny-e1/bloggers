from flask import (render_template, url_for, flash,
                   redirect, request, abort)
from flask_login import current_user, login_required
from app import db
from app.models.models import Draft
from app.drafts.forms import DraftForm
from app.auth.utils import save_picture
from . import drafts


@drafts.route("/drafts")
@login_required
def draft():
    page = request.args.get('page', 1, type=int)
    drafts = Draft.query.order_by(Draft.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('public/draft.html', drafts=drafts)

@drafts.route("/draft/<int:draft_id>/update", methods=['GET', 'POST'])
@login_required
def update_draft(post_id):
    draft = Draft.query.get_or_404(post_id)
    if draft.author != current_user:
        abort(403)
    form = DraftForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            draft.title = form.title.data
            draft.content = form.content.data
            db.session.commit()
            flash('Your post has been updated!', 'success')
            return redirect(url_for('drafts.draft', draft_id=draft.id))
    elif request.method == 'GET':
        form.title.data = draft.title
        form.description.data = draft.description
        form.tag.data = draft.data
        form.picture.data = draft.picture
        form.content.data = draft.content
    return render_template('public/post_draft.html',
                           form=form, legend='post draft')


@drafts.route("/draft/<int:draft_id>/delete", methods=['POST'])
@login_required
def delete_draft(draft_id):
    draft = Draft.query.get_or_404(post_id)
    if draft.author != current_user:
        abort(403)
    db.session.delete(draft)
    db.session.commit()
    flash('Your draft has been deleted!', 'success')
    return redirect(url_for('drafts.draft'))
