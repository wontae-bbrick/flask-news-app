from flask import Flask, Blueprint
from flask_restful import Api
from apscheduler.schedulers.background import BackgroundScheduler
from app.routes import bp
from app.db_connector import db
from app.controllers.news.ai import AiController, AiListController
from app.controllers.news.sto import StoController, StoListController
from config import Config
from app.crawlers.naver import run as naver_run

def crawl():
    naver_run('ai')
    naver_run('sto')

crawler = BackgroundScheduler(daemon=True, timezone='Asia/Seoul')
crawler.add_job(crawl, 'interval', seconds=2)
crawler.start()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initiate database
    db.init_app(app)

    # Register APIs
    api = Api(app)
    api.add_resource(AiListController, '/ai')
    api.add_resource(AiController, '/ai/<id>')
    api.add_resource(StoListController, '/sto')
    api.add_resource(StoController, '/sto/<id>')
    # Register blueprints here
    # 각각 ai, sto, 해서 url_prefix를 주면 되겠
    # 습니다
    # bp = Blueprint('main', __name__, url_prefix='/')
    app.register_blueprint(bp)

    return app