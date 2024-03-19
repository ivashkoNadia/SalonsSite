import re
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    type_user = db.Column(db.String(50))
    phone = db.Column(db.String(20))

    def __init__(self, name, email, password, type_user, phone):
        self.name = name
        self.email = email
        self.password = password
        self.type_user = type_user
        self.phone = phone

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def validate_user(self):
        errors = {
            "name": "",
            "email": "",
            "password": "",
            "phone": "",
            "message":""
        }

        if any(char.isdigit() for char in self.name):
            errors["name"]="Ім'я повинно містити тільки букви"

        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            errors["email"]="Введіть дійсний email"

        if len(self.password) < 8 or not any(char.isdigit() for char in self.password) or not any(
                char.isalpha() for char in self.password):
            errors["password"]="Пароль повинен містити цифри і букви, мінімум 8 символів"

        if len(self.phone) != 10 or not self.phone.isdigit():
            errors["phone"]="Введіть дійсний номер"

        return errors

    def check_email_exists(self):
        user_with_email = User.query.filter_by(email=self.email).first()

        if user_with_email:
            return True
        else:
            return False


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

class Appointment(db.Model):
    __tablename__ = 'Appointments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    salon_id = db.Column(db.Integer,  nullable=False)
    service_id = db.Column(db.Integer,  nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, salon_id, service_id, datetime):
        self.salon_id=salon_id
        self.service_id=service_id
        self.user_id=user_id
        self.datetime=datetime

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class Service(db.Model):
    __tablename__ = 'Services'
    id = db.Column(db.Integer, primary_key=True)
    salon_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

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