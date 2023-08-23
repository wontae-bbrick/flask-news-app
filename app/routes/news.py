from flask import request
from app.routes import bp
from app.controllers.news import NewsController, NewsListController

@bp.route('/news/<string:keyword>', methods=['GET, POST'])
def newsList(keyword):
    newslistController = NewsListController(keyword)
    if request.method == 'GET':
        # keyword가 없으면 새로 만들어야함. 컨트롤러 안에서!
        newslistController.get()
    else:
        newslistController.post()

@bp.route('/news/<string:keyword>/<string:id>', methods=['GET, DELETE'])
def news(keyword, id):
    newsController = NewsController(keyword)

    if request.method == 'GET':
        newsController.get(id)
    else:
        newsController.delete(id)