from Entity.User import  db
class Service(db.Model):
    __tablename__ = 'Services'
    id = db.Column(db.Integer, primary_key=True)
    salon_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
