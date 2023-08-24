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
from app.crawlers.naver import *
from app.crawlers.daum import *
from app.crawlers.google import *

import datetime
import requests

# 다이나믹하게...
crawlers = []
class_methods = {
    "__init__": lambda self, keyword: setattr(self, "keyword", keyword),
}

def get_keywords():
    # 런타임에서 만들 수 있게
    # args로 중복 안되게 보낸다던가 하는거
    res = requests.get(f'http://127.0.0.1:5000/keyword')
    data = res.json()
    for each in data:
        keyword = each['keyword']
        newsCrawler = type("DaumNewsCrawler", (object,), {**class_methods})
        crawlers.append(newsCrawler(keyword))
        pass
    print(crawlers)

    return data

def crawl():
    for crawler in crawlers:
        # crawler().run()
        pass
    # naverNewsAi.run()
    # naverNewsSto.run()
    # daumNewsAi.run()
    # daumNewsSto.run()
    # googleNewsAi.run()
    # googleNewsSto.run()
    pass

# 가져오는건 한번만 하면 되나? 어떻게 하면 좋을까?
crawler = BackgroundScheduler(daemon=True, timezone='Asia/Seoul')
# 이거 한번만?
crawler.add_job(get_keywords, 'date', run_date=datetime.datetime.now() + datetime.timedelta(seconds=1))
crawler.add_job(crawl, 'interval', seconds=5)
crawler.start()

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