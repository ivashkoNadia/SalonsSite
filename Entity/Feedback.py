from Entity.User import db

class Feedback(db.Model):
    __tablename__ = 'Feedback'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text)
    datetime = db.Column(db.TIMESTAMP)
    rating = db.Column(db.Integer)
    salon_id = db.Column(db.Integer)

    def __init__(self, user_id, text, rating, salon_id, datetime):
        self.user_id = user_id
        self.text = text
        self.rating = rating
        self.salon_id = salon_id
        self.datetime=datetime

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()