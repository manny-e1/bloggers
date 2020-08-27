import os



class Config(object):
    SECRET_KEY = "asdfghjkl1234567890"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'tsionambe@gmail.com'
    MAIL_PASSWORD = 'anteneh23'
    SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://postgres:anteneh23@localhost:5432/blogger'
    CKEDITOR_SERVE_LOCAL = False
    CKEDITOR_HEIGHT = 400
    CKEDITOR_FILE_UPLOADER = 'upload'
    FLASK_ADMIN_SWATCH ='yeti'


    
class DevelopmentConfig(Config):
    DEBUG = True
    pass


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}