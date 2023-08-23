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





def crawl():
    


    # naverNewsAi.run()
    # naverNewsSto.run()
    # daumNewsAi.run()
    # daumNewsSto.run()
    # googleNewsAi.run()
    # googleNewsSto.run()
    pass

crawler = BackgroundScheduler(daemon=True, timezone='Asia/Seoul')
crawler.add_job(crawl, 'interval', seconds=5)
# crawler.start()

def get_keywords():

    pass


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