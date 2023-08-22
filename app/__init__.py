from flask import Flask, Blueprint
from flask_restful import Api
from apscheduler.schedulers.background import BackgroundScheduler
from app.routes import bp
from app.db_connector import db
from app.controllers.news.ai import AiController, AiListController
from app.controllers.news.sto import StoController, StoListController
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
    googleNewsAi.run()
    googleNewsSto.run()

crawler = BackgroundScheduler(daemon=True, timezone='Asia/Seoul')
crawler.add_job(crawl, 'interval', seconds=5)
crawler.start()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    api = Api(app)
    api.add_resource(AiListController, '/ai')
    api.add_resource(AiController, '/ai/<id>')
    api.add_resource(StoListController, '/sto')
    api.add_resource(StoController, '/sto/<id>')
    app.register_blueprint(bp)

    return app