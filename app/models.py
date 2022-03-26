from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
    
    
class Question(db.Model):
    __tablename__ = 'question'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    
class Answer(db.Model):
    __tablename__ = 'answer'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(250), nullable=False)

class CustomerAnswer(db.Model):
    __tablename__ = 'customeranswer'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, nullable=False)
    answer_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    
class Customer(db.Model):
    __tablename__ = 'customer'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=False)
    eamill = db.Column(db.String(250), nullable=False)
    job = db.Column(db.String(250), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    income = db.Column(db.Integer, nullable=False)
    