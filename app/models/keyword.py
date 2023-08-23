from app.db_connector import db

class Keyword(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'{self.id}번 Keyword: {self.name}'
