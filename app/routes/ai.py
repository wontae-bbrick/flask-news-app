from flask import request
from app.routes import bp
from app.controllers.news.ai import aiController, aiListController

@bp.route('/ai', methods=('GET, POST'))
def index():
    if request.method == 'GET':
        aiListController.get()
    else:
        aiListController.post()

@bp.route('/ai/<string: id>', methods=('GET, DELETE'))
def ai(id):
    if request.method == 'GET':
        aiController.get(id)
    else:
        aiController.delete(id)