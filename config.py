import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:wtchoe13@localhost:3306/news_crawler'
        # or 'mysql+pymysql:///root:비밀번호아닌가?@localhost:3306/news_crawler'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False