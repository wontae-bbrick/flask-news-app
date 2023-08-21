from flask import request
from app.routes import bp
from app.controllers.news.ai import AiController, AiListController

aiController = AiController()
aiListController = AiListController()
@bp.route('/ai', methods=['GET, POST'])
def aiList():
    if request.method == 'GET':
        aiListController.get()
    else:
        aiListController.post()

@bp.route('/ai/<string:id>', methods=['GET, DELETE'])
def ai(id):
    if request.method == 'GET':
        aiController.get(id)
    else:
        aiController.delete(id)