from flask import request
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from app.models.news import News
from app.db_connector import db

news_args = reqparse.RequestParser()

news_args.add_argument('keyword',
                            type=str,
                            help="Error: keyword is required.",
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
    'id': fields.Integer,
    'title': fields.String,
    'keyword': fields.String,
    'platform': fields.String,
    'press': fields.String,
    'datetime': fields.String,
    'url': fields.String,
    'deleted': fields.Boolean
}

class NewsListController(Resource):
    def __init__(self, keyword):
        self.keyword = keyword

    @marshal_with(news_fields)
    def get(self):
        args = request.args
        platform = args.get('platform')
        latest = args.get('latest', default='false').lower() == 'true'
        if latest:
            result = News.query.filter(News.keyword==self.keyword, News.platform==platform, News.deleted==False).order_by(News.id.desc()).first()
        else:
            result = News.query.filter(News.keyword==self.keyword, News.deleted==False).all()
        return result

    @marshal_with(news_fields)
    def post(self):
        args = news_args.parse_args() 
        news = News(
            keyword=self.keyword,
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
    def __init__(self, keyword):
        self.keyword = keyword
        
    @marshal_with(news_fields)
    def get(self, id):
        result = News.query.filter(News.keyword==self.keyword, News.id==id).first()
        if not result:
            abort(404, message=f"{self.keyword} with id: {id} does not exist.")
        if result.deleted:
            abort(404, message=f"{self.keyword} with id: {id} is already deleted.")
        return result

    @marshal_with(news_fields)
    def delete(self, id):
        existing_news = News.query.filter(News.keyword==self.keyword, News.id==id).first()
        if not existing_news:
            abort(404, message=f"{self.keyword} with id: {id} does not exist.")
        elif existing_news.deleted == True:
            abort(404, message=f"{self.keyword} with id: {id} has been already deleted.")
        else:
            existing_news.deleted = True
            db.session.commit()
            return existing_news