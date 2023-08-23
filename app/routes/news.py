from flask import request
from app.routes import bp
from app.controllers.news import NewsController, NewsListController

newsController = NewsController()
newsListController = NewsListController()
@bp.route('/news/<string:keyword>', methods=['GET, POST'])
def newsList(keyword):
    if request.method == 'GET':
        newsListController.get(keyword)
    else:
        newsListController.post(keyword)

@bp.route('/news/<string:keyword>/<string:id>', methods=['GET, DELETE'])
def news(keyword, id):
    newsController = NewsController(keyword)

    if request.method == 'GET':
        newsController.get(keyword, id)
    else:
        newsController.delete(keyword, id)