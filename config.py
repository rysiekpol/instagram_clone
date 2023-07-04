import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "sóper-tródne-hałso"
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_USERNAME = "o396"
    DB_PASSWORD = os.environ.get("DATABASE_PASSWORD")
    DB_HOST = os.environ.get("DATABASE_HOST")
    DB_PORT = 3306
    DB_NAME = "db_o396"

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    MAIL_SERVER = "mailhog"
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    ADMINS = ["admin@example.com"]
    POSTS_PER_PAGE = 25
    UPLOADS_DEFAULT_DEST = os.environ.get("UPLOADS_DEFAULT_DEST")
