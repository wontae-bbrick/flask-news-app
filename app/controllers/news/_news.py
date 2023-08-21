from app.models.news import News
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from app.db_connector import db

news_post_args = reqparse.RequestParser()
news_post_args.add_argument('category',
                            type=str,
                            help="Error: category is required.",
                            required=True)
news_post_args.add_argument('platform',
                            type=str,
                            help="Error: platform is required.",
                            required=True)
news_post_args.add_argument('press',
                            type=str,
                            help="Error: press is required.",
                            required=True)
news_post_args.add_argument('datetime',
                            type=int,
                            help="Error: datetime is required.",
                            required=True)
news_post_args.add_argument('url',
                            type=str,
                            help="Error: url is required.",
                            required=True)
news_post_args.add_argument('deleted',
                            type=bool,
                            required=False)

news_fields = {
    'id': fields.Integer,
    'category': fields.String,
    'platform': fields.String,
    'press': fields.String,
    'datetime': fields.Integer,
    'url': fields.String,
    'deleted': fields.Boolean
}

class NewsListController(Resource):
    category = ''
    
    @marshal_with(news_fields)
    def get(self):
        result = News.query.filter(News.category==self.category, News.deleted==False).all()
        return result

    @marshal_with(news_fields)
    def post(self):
        args = news_post_args.parse_args()
        news = News(
            category=self.category,
            platform=args['platform'],
            press=args['press'],
            datetime=args['datetime'],
            url=args['url'],
        )
        db.session.add(news)
        db.session.commit()
        return news
    
# 이걸 상속을 해줘야한다

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