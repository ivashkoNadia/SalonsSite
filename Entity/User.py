from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask import request
import  main_data
from flask_cors import CORS
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
