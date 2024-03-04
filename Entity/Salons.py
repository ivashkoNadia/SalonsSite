from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Salon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    district = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)