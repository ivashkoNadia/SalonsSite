from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import feedback
import appointment
from Entity.User import User, Salon, Service, Appointment, Feedback, db
# from Entity.Salons import Salon, db
import main_data
import base64
import json
from datetime import datetime, timedelta
# db = SQLAlchemy()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = main_data.DB_CONNECTION
# db = SQLAlchemy(app)  # Ініціалізуємо об'єкт SQLAlchemy
db.init_app(app)

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('user_name')
    email = data.get('user_email')
    password = data.get('user_password')
    phone = data.get('user_phone')
    type_user = data.get('user_account_type')

    new_user = User(name=name, email=email, password=password, type_user=type_user, phone=phone)
    errors = new_user.validate_user()
    if all(value == "" for value in errors.values()):
        if new_user.check_email_exists():
            errors["message"]="Користувач з такою адресою вже існує"
            return jsonify({'errors': errors})
        new_user.save_to_db()
        return  jsonify({'message': "Користувач успішно зареєстрований"})

    return jsonify({'errors': errors})



@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
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

@app.route('/get_our_user', methods=['GET'])
def get_our_user():
    data = request.get_json()
    user_id = data.get('user_id')  # Отримуємо id користувача для редагування
    user = User.query.filter_by(user_id=user_id).first()
    print(user.name)
    return jsonify({
        'user_id': user.user_id,
        'name': user.name,
        'email': user.email,
        'type_user': user.type_user,
        'phone': user.phone
    })


@app.route('/edit_user', methods=['POST'])
def edit_user():
    data = request.get_json()
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

@app.route('/edit_user_password', methods=['POST'])
def edit_user_password():
    data = request.get_json()
    user_id = data.get('user_id')  # Отримуємо id користувача для редагування
    password = data.get('password')
    new_password = data.get('new_password')

    if password=="" or new_password=="": return jsonify({'error': 'Ви ввели не всі дані'})

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



@app.route('/available_salons', methods=['GET'])
def get_salons_availavle():
    salons = Salon.query.filter_by(approve=1).all()

    salon_data = [{'id': salon.id, 'district': salon.district, 'name': salon.name, 'rating': salon.rating,
                   'photo': base64.b64encode(salon.photo).decode('utf-8') if salon.photo else None} for salon in salons]

    return jsonify({'salons': salon_data})


@app.route('/add_photo_to_salon')
def add_photo_to_salon():
    salon = Salon.query.filter_by(id=1).first()
    if salon:
        photo_path = "C:/Users/Nadiia/Desktop/_17_.png"
        # C:\Users\Nadiia\Downloads
        with open(photo_path, "rb") as photo_file:
            salon.photo = photo_file.read()
        db.session.commit()
        return "Фото успішно додано до салону"
    else:
        return "Салон з вказаним id не знайдено"


@app.route('/salon_details', methods=['POST'])
def salon_details():
    data = request.get_json()
    salon_id = data.get('salon_id')
    # salon = Salon.query.get(int(salon_id))
    salon = db.session.get(Salon, int(salon_id))

    if salon:
        salon_data = {
            "id": salon.id,
            "district": salon.district,
            "name": salon.name,
            'photo': base64.b64encode(salon.photo).decode('utf-8') if salon.photo else None,
            "rating": salon.rating,
            "approve": salon.approve,
            "street": salon.street,
            "social": salon.social
        }
        return jsonify({'salon': salon_data})
    else:
        return jsonify({'error': 'Салон з вказаним ID не знайдено'})

@app.route('/salon_services', methods=['POST'])
def salon_services():
    data = request.get_json()
    salon_id = data.get('salon_id')
    salon_services = Service.query.filter_by(salon_id=int(salon_id)).all()

    if not salon_services:
        return jsonify({'message': 'No services found for the specified salon ID'}), 404

    serialized_services = []
    for service in salon_services:
        serialized_services.append({
            'id': service.id,
            'salon_id': service.salon_id,
            'name': service.name,
            'price': service.price
        })

    # Return the serialized services
    return jsonify({'services':serialized_services})



@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    data = request.get_json()
    user_id = data.get('user_id')
    salon_id = data.get('salon_id')
    service_id = data.get('service_id')
    appointment_datetime = data.get('datetime')

    # Перевірка, чи не існує вже запису на цей день та час для цього користувача та процедури
    existing_appointment = Appointment.query.filter_by(salon_id=salon_id, service_id=service_id,
                                                       datetime=appointment_datetime).first()
    if existing_appointment:
        available_hours = []
        for hour in range(9, 20, 2):  # Перевіряємо години з 09:00 до 19:00 з інтервалом 2 години
            new_datetime = datetime.strptime(appointment_datetime, '%Y-%m-%d %H:%M').replace(hour=hour,
                                                                                             minute=0)  # Встановлюємо годину та хвилину
            new_datetime_str = new_datetime.strftime('%Y-%m-%d %H:%M')
            existing_appointment = Appointment.query.filter_by(salon_id=salon_id, service_id=service_id,
                                                               datetime=new_datetime).first()
            if not existing_appointment:
                split_string = new_datetime_str.split(' ')
                # Отримання години
                hour_ = split_string[1]
                available_hours.append(hour_)
        str_m= "Запис на цей час процедури вже існує \n Доступні години в цей день:"+str(available_hours)
        return jsonify({'error': str_m})

    # Перевірка, щоб запис не був раніше ніж за 2 години вперед
    current_datetime = datetime.now()
    appointment_datetime_obj = datetime.strptime(appointment_datetime, '%Y-%m-%d %H:%M')
    if appointment_datetime_obj < current_datetime + timedelta(hours=2):
        return jsonify({'error': 'Неможливо записатися раніше, ніж за дві години від поточного часу'})

    user_id_dict = json.loads(user_id)
    user_id = user_id_dict['user_id']

    # Створення нового запису
    new_appointment = Appointment(user_id=user_id, salon_id=salon_id, service_id=service_id, datetime=appointment_datetime)

    new_appointment.save_to_db()
    return jsonify({'message': 'Запис успішно створений'})

@app.route('/add_feedback', methods=['POST'])
def add_feedback():
    data = request.get_json()
    user_id = data.get('user_id')
    text = data.get('text')
    rating = data.get('rating')
    salon_id = data.get('salon_id')

    user_id_dict = json.loads(user_id)
    user_id = user_id_dict['user_id']

    # # Перевірка обов'язкових полів
    # if not all(rating):
    #     return jsonify({'error': 'Не всі обов\'язкові поля заповнені'})

    # Створення нового об'єкту Feedback
    new_feedback = Feedback(user_id=int(user_id), text=text, rating=int(rating), salon_id=int(salon_id), datetime=datetime.now())

    salon= Salon.query.filter_by(id=int(salon_id)).first()
    rating_amount=salon.rating_amount
    star=salon.rating
    new_rating= (star*rating_amount+rating)/(rating_amount+1)
    salon.rating = new_rating
    salon.rating_amount += 1
    db.session.merge(salon)  # Оновлення користувача
    db.session.commit()

    try:
        # Додавання об'єкту до бази даних
        new_feedback.save_to_db()
        return jsonify({'message': 'Feedback успішно доданий'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Помилка при додаванні feedback'})

@app.route('/salon_feedback', methods=['POST'])
def salon_feedback():
    data = request.get_json()
    return feedback.fun_feedback(data)

@app.route('/user_appointments', methods=['POST'])
def user_appointments():
    data = request.get_json()
    return appointment.fun_user_appointments(data)

if __name__ == '__main__':
    app.run(debug=True)


