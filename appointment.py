from Entity.User import User
from Entity.Salons import Salon
from Entity.Appointment import Appointment
from flask import Flask, request, jsonify
import json
from datetime import datetime, timedelta
import os
from PIL import Image

def fun_add_appointment(data):
    user_id = data.get('user_id')
    salon_id = data.get('salon_id')
    service_name = data.get('service_name')
    appointment_datetime = data.get('datetime')

    # Перевірка, чи не існує вже запису на цей день та час для цього користувача та процедури
    existing_appointment = Appointment.query.filter_by(salon_id=salon_id, service_name=service_name,
                                                       datetime=appointment_datetime).first()
    if existing_appointment:
        available_hours = []
        for hour in range(9, 20, 2):  # Перевіряємо години з 09:00 до 19:00 з інтервалом 2 години
            new_datetime = datetime.strptime(appointment_datetime, '%Y-%m-%d %H:%M').replace(hour=hour,
                                                                                             minute=0)  # Встановлюємо годину та хвилину
            new_datetime_str = new_datetime.strftime('%Y-%m-%d %H:%M')
            existing_appointment = Appointment.query.filter_by(salon_id=salon_id, service_name=service_name,
                                                               datetime=new_datetime).first()
            if not existing_appointment:
                split_string = new_datetime_str.split(' ')
                # Отримання години
                hour_ = split_string[1]
                available_hours.append(hour_)
        str_m = "Запис на цей час процедури вже існує \n Доступні години в цей день:" + str(available_hours)
        return jsonify({'error': str_m})

    # Перевірка, щоб запис не був раніше ніж за 2 години вперед
    current_datetime = datetime.now()
    appointment_datetime_obj = datetime.strptime(appointment_datetime, '%Y-%m-%d %H:%M')
    if appointment_datetime_obj < current_datetime + timedelta(hours=2):
        return jsonify({'error': 'Неможливо записатися раніше, ніж за дві години від поточного часу'})

    user_id_dict = json.loads(user_id)
    user_id = user_id_dict['user_id']

    # Створення нового запису
    new_appointment = Appointment(user_id=user_id, salon_id=salon_id, service_name=service_name,
                                  datetime=appointment_datetime)

    new_appointment.save_to_db()
    return jsonify({'message': 'Запис успішно створений'})

def fun_user_appointments(data):
    user_id = data.get('user_id')

    user_id_dict = json.loads(user_id)
    user_id = user_id_dict['user_id']

    current_datetime = datetime.now()
    # Вибірка записів, де дата і час не раніше поточної дати і часу
    appointments = Appointment.query.filter(
        Appointment.user_id == int(user_id),
        Appointment.datetime >= current_datetime
    ).all()

    # Серіалізуємо дані у вказаний формат
    serialized_appointments = []
    for appointment in appointments:
        salon = Salon.query.filter_by(id=int(appointment.salon_id)).first()
        # service = Service.query.filter_by(id=int(appointment.service_id)).first()
        serialized_appointments.append({
            'salon_name': salon.name,
            'salon_street':salon.street,
            'service_name': appointment.service_name,
            'appointment_id':appointment.id,
            'datetime': appointment.datetime.strftime('%Y-%m-%d %H:%M')  # Перетворення в формат рядка
        })
    # Повертаємо серіалізовані дані у форматі JSON
    return jsonify({'appointments': serialized_appointments})

def fun_delete_appointment(appointment_id, db):
    try:
        # Знаходимо запис за його ідентифікатором
        appointment = Appointment.query.get(appointment_id)

        if appointment:
            if datetime.now() <= (appointment.datetime - timedelta(hours=3)):
                db.session.delete(appointment)
                db.session.commit()
                return jsonify({'message': 'Запис успішно видалено'})
            else:
                return jsonify({'message': 'Запис можна скасувати не пізніше, ніж за 3 години'})
        else:
            return jsonify({'message': 'Запис не знайдено'})

    except Exception as e:
        return jsonify({'message': str(e)})

def fun_client_appointments(data):
    user_id = data.get('user_id')
    user_id_dict = json.loads(user_id)
    user_id = int(user_id_dict['user_id'])

    try:
        # Отримуємо список салонів, що належать користувачеві
        user_salons = Salon.query.filter_by(owner_id=user_id).all()
        if not user_salons:
            return jsonify({'message': 'Користувач не має жодного салону'})

        # Отримуємо id салонів
        salon_ids = [salon.id for salon in user_salons]

        current_datetime = datetime.now()
        # Отримуємо список записів у салонах користувача
        user_appointments = Appointment.query.filter(
            Appointment.salon_id.in_(salon_ids),
            Appointment.datetime >= current_datetime
        ).all()

        # Формуємо список словників з даних про записи користувача
        appointments_data = []
        for appointment in user_appointments:
            user = User.query.get(appointment.user_id)
            salon = Salon.query.get(appointment.salon_id)
            appointments_data.append({
                'user_name': user.name,
                'user_phone': user.phone,
                'salon_name': salon.name,
                'service_name': appointment.service_name,
                'datetime': appointment.datetime.strftime('%Y-%m-%d %H:%M')
            })

        return jsonify({'appointments': appointments_data})

    except Exception as e:
        return jsonify({'error': str(e)})