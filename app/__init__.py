from flask import Flask, Blueprint
from flask_restful import Api
from apscheduler.schedulers.background import BackgroundScheduler
from app.routes import bp
from app.db_connector import db
# from app.controllers.news.ai import AiController, AiListController
# from app.controllers.news.sto import StoController, StoListController
from app.controllers.news import NewsController, NewsListController
from app.controllers.keyword import KeywordController, KeywordListController
from config import Config

# 이것도 다 하나로 모아볼까
# from app.crawlers.naver import *
# from app.crawlers.daum import *
# from app.crawlers.google import *
from app.crawlers import crawlerTypes

import datetime
import requests

crawlers = []

# 추가될때마다
# 이걸 코드를 따로 하고 싶거든요?
# 삭제될 때
# 중복체크
# 런타임에서 만들 수 있게
def get_keywords():
    res = requests.get(f'http://127.0.0.1:5000/keyword')
    data = res.json()
    for crawlerType in crawlerTypes:
        for each in data:
            keyword = each['keyword']
            newsCrawler = type(crawlerType.__class__.__name__, (crawlerType,), {
                "__init__": crawlerType.__init__,
            })
            instance = newsCrawler(keyword)
            crawlers.append(instance)

    return data

def crawl():
    for crawler in crawlers:
        crawler.run()

crawler = BackgroundScheduler(daemon=True, timezone='Asia/Seoul')
crawler.add_job(get_keywords, 'date', run_date=datetime.datetime.now() + datetime.timedelta(seconds=1))
crawler.add_job(crawl, 'date', run_date=datetime.datetime.now() + datetime.timedelta(seconds=5))
# crawler.start()

def get_keywords():
    keywords = requests.get(f'http://127.0.0.1:5000/keyword')
    return keywords


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    api = Api(app)

    api.add_resource(NewsListController, '/news/<keyword>')
    api.add_resource(NewsController, '/news/<keyword>/<id>')
    api.add_resource(KeywordListController, '/keyword')
    api.add_resource(KeywordController, '/keyword/<id>')

    app.register_blueprint(bp)

    # 최초로 한번 보내고 만들어지잖아.
    # 여기서 request.get으로 있는애들 다 만들어와바

    return app