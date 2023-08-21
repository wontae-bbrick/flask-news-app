from app.db_connector import db
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

class News(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    platform = db.Column(db.String, nullable=False)
    press = db.Column(db.String, nullable=False)
    datetime = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(200), unique=True, nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'{self.id}번 category: {self.category}, press: {self.press}, datetime: {self.datetime}, url: {self.url}'
