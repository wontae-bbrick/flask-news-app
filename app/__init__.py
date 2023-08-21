from flask import Flask
from flask_restful import Api
from app.routes import bp as blueprints
from app.db_connector import db
from app.controllers.news.ai import aiController, aiListController
from app.controllers.news.sto import stoController, stoListController
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initiate database
    db.init_app(app)

    # Register APIs
    api = Api(app)
    api.add_resource(aiListController, '/ai')
    api.add_resource(aiController, '/ai/<id>')
    api.add_resource(stoListController, '/sto')
    api.add_resource(stoController, '/sto/<id>')
    # Register blueprints here
    # 각각 ai, sto, 해서 url_prefix를 주면 되겠
    # 습니다
    app.register_blueprint(blueprints)

    return app