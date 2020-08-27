from flask import Flask
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, form, AdminIndexView
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config
from flask_migrate import Migrate
from flask_compress import Compress
from flask_ckeditor import CKEditor
from app.config import Config
COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500


# bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
migrate = Migrate()
mail = Mail()
compress = Compress()
db = SQLAlchemy()
ckeditor = CKEditor()





def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    mail.init_app(app)
    compress.init_app(app)
    ckeditor.init_app(app)

    admin.init_app(app)

    from app.models.models import Comment
    admin.add_view(UserView(User,db.session))
    admin.add_view(PostView(Post,db.session))
    admin.add_view(CommentView(Comment,db.session))



    from app.auth import users
    from app.posts import posts
    from app.main import main
    from app.api import api
    # from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix='/api')
    # app.register_blueprint(errors)

    return app



from flask_admin.contrib.sqla import ModelView
from flask_ckeditor import CKEditorField
from app.models.models import User,Post,Comment
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from flask_admin.form.upload import FileUploadField, ImageUploadField
import os


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class PostView(ModelView):  
    def is_accessible(self):
        return current_user.is_authenticated and current_user.isAdmin
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'content': CKTextAreaField
    }
    form_extra_fields = {
        'cover_image': form.ImageUploadField('Cover Image',
                    base_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'cover_images'))
    }


class UserView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.isAdmin  
    form_excluded_columns = ('password')
    #
    form_extra_fields = {
        'image_file': form.ImageUploadField('Profile Pic',
                    base_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'profile_pics'))
       
    }
      
    form_columns = (
        'username',
        'email',
        'password',
        'confirmed',
        'isAdmin',
        'image_file'
    )

    def on_model_change(self, form, User, is_created):
        if form.password.data is not None:
            User.set_password(form.password.data)



class CommentView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.isAdmin
class IndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.isAdmin

admin = Admin(name='Bloggers', template_mode='bootstrap3', index_view=IndexView())