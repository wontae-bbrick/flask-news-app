from flask import request
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from app.models.news import News
from app.db_connector import db

news_args = reqparse.RequestParser()
# news_args.add_argument('latest', type=bool, location='args', required=False)

news_args.add_argument('category',
                            type=str,
                            help="Error: category is required.",
                            required=True)
news_args.add_argument('title',
                            type=str,
                            help="Error: title is required.",
                            required=True)
news_args.add_argument('platform',
                            type=str,
                            help="Error: platform is required.",
                            required=True)
news_args.add_argument('press',
                            type=str,
                            help="Error: press is required.",
                            required=True)
news_args.add_argument('datetime',
                            type=str,
                            help="Error: datetime is required.",
                            required=True)
news_args.add_argument('url',
                            type=str,
                            help="Error: url is required.",
                            required=True)
news_args.add_argument('deleted',
                            type=bool,
                            required=False)

news_fields = {
    # 'latest': fields.Boolean,
    'id': fields.Integer,
    'title': fields.String,
    'category': fields.String,
    'platform': fields.String,
    'press': fields.String,
    'datetime': fields.String,
    'url': fields.String,
    'deleted': fields.Boolean
}

class NewsListController(Resource):
    category = ''
    
    @marshal_with(news_fields)
    def get(self):
        args = request.args
        platform = args.get('platform')
        latest = args.get('latest', default='false').lower() == 'true'
        # 여기서 플랫폼이 들어가야함
        if latest:
            result = News.query.filter(News.category==self.category, News.platform==platform, News.deleted==False).order_by(News.id.desc()).first()
        else:
            result = News.query.filter(News.category==self.category, News.deleted==False).all()
        return result

    @marshal_with(news_fields)
    def post(self):
        args = news_args.parse_args() 
        news = News(
            category=self.category,
            title=args['title'],
            platform=args['platform'],
            press=args['press'],
            datetime=args['datetime'],
            url=args['url'],
        )
        db.session.add(news)
        db.session.commit()
        return news

class NewsController(Resource):
    category = ''
    @marshal_with(news_fields)
    def get(self, id):
        result = News.query.filter(News.category==self.category, News.id==id).first()
        if not result:
            abort(404, message=f"{self.category} with id: {id} does not exist.")
        if result.deleted:
            abort(404, message=f"{self.category} with id: {id} is already deleted.")
        return result

    @marshal_with(news_fields)
    def delete(self, id):
        existing_news = News.query.filter(News.category==self.category, News.id==id).first()
        if not existing_news:
            abort(404, message=f"{self.category} with id: {id} does not exist.")
        elif existing_news.deleted == True:
            abort(404, message=f"{self.category} with id: {id} has been already deleted.")
        else:
            existing_news.deleted = True
            db.session.commit()
            return existing_news