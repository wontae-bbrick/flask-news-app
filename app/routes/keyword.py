from flask import request
from app.routes import bp
from app.controllers.keyword import KeywordListController

keywordListController = KeywordListController()
@bp.route('/keyword', methods=['GET, POST'])
def keywordList():
    if request.method == 'GET':
        keywordListController.get()
    else:
        keywordListController.post()

# @bp.route('/ai/<string:id>', methods=['GET, DELETE'])
# def ai(id):
#     if request.method == 'GET':
#         aiController.get(id)
#     else:
#         aiController.delete(id)