from app.db_connector import db

class Platform(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String, nullable=False)
    base_url = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f'{self.id}번 Platform: {self.platform}, base_url: {self.base_url}'
