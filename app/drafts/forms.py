from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import SelectField
from wtforms.validators import DataRequired

dropdown = [('Software','Software'),('Technology',"Technology"),('Life Style','Life Style'),('Food','Food')]
class DraftForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    tag = SelectField('tag', choices = dropdown, validators=[DataRequired()])
    picture = FileField('Cover Image', validators=[FileAllowed(['jpg', 'png'])])
    content = TextAreaField('Content', validators=[DataRequired()])
    updateDraft = SubmitField('Update Draft')
    deleteDratt = SubmitField('Delete Draft')
    submit = SubmitField('Post')