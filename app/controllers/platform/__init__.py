from flask import request
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from app.models.platform import Platform
from app.db_connector import db


keyword_args = reqparse.RequestParser()

keyword_args.add_argument('platform',
                            type=str,
                            help="Error: platform is required.",
                            required=True)

keyword_args.add_argument('base_url',
                            type=str,
                            help="Error: base_url is required.",
                            required=True)

keyword_fields = {
    'platform': fields.String,
    'base_url': fields.String,
}

class PlatformListController(Resource):
    @marshal_with(keyword_fields)
    def get(self):
        args = request.args
        search = args.get('search')
        if search:
            result = Platform.query.filter(Platform.search.contains(search), Platform.deleted==False).all()
        else:
            result = Platform.query.filter(Platform.deleted==False).all()
        return result

    @marshal_with(keyword_fields)
    def post(self):
        args = keyword_args.parse_args() 
        existing_search = Platform.query.filter(Platform.platform==args['platform']).first()
        if existing_search:
            abort(409, message=f"platform with {args['platform']} already exist")
        keyword = Platform(
            platform=args['platform'],
            base_url=args['base_url'],
        )
        db.session.add(keyword)
        db.session.commit()
        return keyword

class PlatformController(Resource):
    @marshal_with(keyword_fields)
    def get(self, id):
        result = Platform.query.filter(Platform.id==id).first()
        if not result:
            abort(404, message=f"Keyword with id: {id} does not exist.")
        if result.deleted:
            abort(404, message=f"Keyword with id: {id} is already deleted.")
        return result

    @marshal_with(keyword_fields)
    def delete(self, id):
        existing_keyword = Platform.query.filter(Platform.id==id).first()
        if not existing_keyword:
            abort(404, message=f"Platform with id: {id} does not exist.")
        elif existing_keyword.deleted == True:
            abort(404, message=f"Platform with id: {id} has been already deleted.")
        else:
            existing_keyword.deleted = True
            db.session.commit()
            return existing_keyword