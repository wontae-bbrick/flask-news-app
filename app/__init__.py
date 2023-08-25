from flask import Flask, Blueprint
from flask_restful import Api
from apscheduler.schedulers.background import BackgroundScheduler
from app.routes import bp
from app.db_connector import db
from app.controllers import *
from config import Config

import datetime
from app.services.crawler import CrawlerService

crawlerService = CrawlerService()

scheduler = BackgroundScheduler(daemon=True, timezone='Asia/Seoul')
scheduler.add_job(crawlerService.readyAllCrawlers, 'date', run_date=datetime.datetime.now() + datetime.timedelta(seconds=1))
scheduler.add_job(crawlerService.runAllCrawlers, 'date', run_date=datetime.datetime.now() + datetime.timedelta(seconds=4))
scheduler.add_job(crawlerService.readyAllCrawlers, 'interval', seconds=1200)
scheduler.add_job(crawlerService.runAllCrawlers, 'interval', seconds=600)
scheduler.start()

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
    # crawlerService.readyAllCrawlers()
    return app