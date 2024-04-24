from Entity.User import db

class Appointment(db.Model):
    __tablename__ = 'Appointments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    salon_id = db.Column(db.Integer,  nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    service_name = db.Column(db.Text, nullable=False)

    def __init__(self, user_id, salon_id, service_name, datetime):
        self.salon_id=salon_id
        self.service_name=service_name
        self.user_id=user_id
        self.datetime=datetime

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
