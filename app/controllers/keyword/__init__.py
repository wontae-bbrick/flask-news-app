from flask import request
from flask_restful import Resource, reqparse, abort, fields, marshal_with, inputs
from app.models.keyword import Keyword
from app.db_connector import db


keyword_args = reqparse.RequestParser()

keyword_args.add_argument('keyword',
                            type=str,
                            # type=inputs.regex(r'^[a-zA-Z]+$'),
                            help="Error: keyword is required.",
                            required=True)
# keyword_args.add_argument('search',
#                             type=str,
#                             help="Error: search is required.",
#                             required=True)
keyword_args.add_argument('deleted',
                            type=bool,
                            required=False)

keyword_fields = {
    'id': fields.Integer,
    'keyword': fields.String,
    # 'search': fields.String,
    'deleted': fields.Boolean
}

class KeywordListController(Resource):
    @marshal_with(keyword_fields)
    def get(self):
        args = request.args
        search = args.get('search')
        if search:
            result = Keyword.query.filter(Keyword.search.contains(search), Keyword.deleted==False).all()
        else:
            result = Keyword.query.filter(Keyword.deleted==False).all()
        return result

    @marshal_with(keyword_fields)
    def post(self):
        args = keyword_args.parse_args() 
        existing_search = Keyword.query.filter(Keyword.keyword==args['keyword']).first()
        if existing_search:
            abort(409, message=f"Keyword with {args['keyword']} already exist")
        keyword = Keyword(
            keyword=args['keyword'],
            # search=args['search'],
        )
        db.session.add(keyword)
        db.session.commit()
        return keyword

class KeywordController(Resource):
    @marshal_with(keyword_fields)
    def get(self, id):
        result = Keyword.query.filter(Keyword.id==id).first()
        if not result:
            abort(404, message=f"Keyword with id: {id} does not exist.")
        if result.deleted:
            abort(404, message=f"Keyword with id: {id} is already deleted.")
        return result

    @marshal_with(keyword_fields)
    def delete(self, id):
        existing_keyword = Keyword.query.filter(Keyword.id==id).first()
        if not existing_keyword:
            abort(404, message=f"Keyword with id: {id} does not exist.")
        elif existing_keyword.deleted == True:
            abort(404, message=f"Keyword with id: {id} has been already deleted.")
        else:
            existing_keyword.deleted = True
            db.session.commit()
            return existing_keyword