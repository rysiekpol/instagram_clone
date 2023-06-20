import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sóper-tródne-hałso'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "mailhog"
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL= False
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    ADMINS = ['admin@example.com']
    POSTS_PER_PAGE = 25