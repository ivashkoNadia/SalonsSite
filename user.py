from Entity.Appointment import Appointment
from Entity.Service import Service
from Entity.Salons import Salon
from Entity.User import User
from flask import Flask, request, jsonify
import json
import io
import base64
from PIL import Image

def fun_add_user(data):
    name = data.get('user_name')
    email = data.get('user_email')
    password = data.get('user_password')
    phone = data.get('user_phone')
    type_user = data.get('user_account_type')

    new_user = User(name=name, email=email, password=password, type_user=type_user, phone=phone)
    errors = new_user.validate_user()
    if all(value == "" for value in errors.values()):
        if new_user.check_email_exists():
            errors["message"] = "Користувач з такою адресою вже існує"
            return jsonify({'errors': errors})
        new_user.save_to_db()
        return jsonify({'message': "Користувач успішно зареєстрований"})

    return jsonify({'errors': errors})

def fun_login_user(data):
    email = data.get('user_email')
    password = data.get('user_password')

    if not email or not password:
        return jsonify({'error': 'Введіть дані для входу'})

    user = User.query.filter_by(email=email).first()

    if not user or not user.password == password:
        return jsonify({'error': 'Користувача не знайдено'})

    # return jsonify({'message': 'Успішний вхід'})
    return jsonify({
        'user_id': user.user_id,
        'name': user.name,
        'email': user.email,
        'type_user': user.type_user,
        'phone': user.phone
    })

def fun_edit_user(data, db):
    user_id = data.get('user_id')  # Отримуємо id користувача для редагування
    name = data.get('name')
    phone = data.get('phone')

    # Шукаємо користувача за його id в базі даних
    user_to_edit = User.query.filter_by(user_id=user_id).first()

    if user_to_edit:
        if name:
            user_to_edit.name = name

        if phone:
            user_to_edit.phone = phone

        errors = user_to_edit.validate_user()
        if all(value == "" for value in errors.values()):
            db.session.merge(user_to_edit)  # Оновлення користувача
            db.session.commit()
            return jsonify({'message': "Дані користувача успішно оновлено"})
        else:
            return jsonify({'errors': errors})
    else:
        return jsonify({'error': 'Користувача з таким id не знайдено'})

def fun_edit_user_password(data, db):
    user_id = data.get('user_id')  # Отримуємо id користувача для редагування
    password = data.get('password')
    new_password = data.get('new_password')

    if password == "" or new_password == "": return jsonify({'error': 'Ви ввели не всі дані'})

    user_to_edit = User.query.filter_by(user_id=user_id).first()
    if user_to_edit.password != password: return jsonify({'error': 'Ви ввели не правильний пароль'})

    if user_to_edit:
        user_to_edit.password = new_password
        errors = user_to_edit.validate_user()
        if all(value == "" for value in errors.values()):
            db.session.merge(user_to_edit)  # Оновлення користувача
            db.session.commit()
            return jsonify({'message': "Дані користувача успішно оновлено"})
        else:
            return jsonify({'error': 'Новий пароль повинен містити цифри і букви, мінімум 8 символів'})
    else:
        return jsonify({'error': 'Користувача з таким id не знайдено'})