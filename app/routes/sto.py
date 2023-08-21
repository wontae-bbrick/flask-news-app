from flask import request
from app.routes import bp
from app.controllers.news.sto import StoController, StoListController


stoController = StoController()
stoListController = StoListController()
@bp.route('/sto', methods=['GET, POST'])
def stoList():
    if request.method == 'GET':
        stoListController.get()
    else:
        stoListController.post()

@bp.route('/sto/<string:id>', methods=['GET, DELETE'])
def sto(id):
    if request.method == 'GET':
        stoController.get(id)
    else:
        stoController.delete(id)