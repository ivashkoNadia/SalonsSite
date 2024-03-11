# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()
#
# class Service(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     salon_id = db.Column(db.Integer, db.ForeignKey('salon.id'), nullable=False)
#     name = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Float, nullable=False)