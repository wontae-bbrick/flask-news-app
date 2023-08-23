from flask import request
from app.routes import bp
from app.controllers.keyword import KeywordListController, KeywordController

keywordController = KeywordController()
keywordListController = KeywordListController()
@bp.route('/keyword', methods=['GET, POST'])
def keywordList():
    if request.method == 'GET':
        keywordListController.get()
    else:
        keywordListController.post()

@bp.route('/keyword/<string:id>', methods=['GET, DELETE'])
def keyword(id):
    if request.method == 'GET':
        keywordListController.get(id)
    else:
        keywordListController.delete(id)