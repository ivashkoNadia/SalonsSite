from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Salon(db.Model):
    __tablename__ = 'Salons'
    id = db.Column(db.Integer, primary_key=True)
    district = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float)
    approve = db.Column(db.Integer)
    photo = db.Column(db.LargeBinary)