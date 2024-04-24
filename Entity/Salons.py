from Entity.User import db

class Salon(db.Model):
    __tablename__ = 'Salons'
    id = db.Column(db.Integer, primary_key=True)
    district = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float)
    approve = db.Column(db.Integer)
    photo = db.Column(db.LargeBinary)
    street = db.Column(db.Text)
    social = db.Column(db.Text)
    rating_amount = db.Column(db.Integer)
    owner_id = db.Column(db.Integer)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()