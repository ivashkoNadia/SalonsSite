# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()
# class Appointment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     salon_id = db.Column(db.Integer, db.ForeignKey('salon.id'), nullable=False)
#     service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
#     datetime = db.Column(db.DateTime, nullable=False)
