from Entity.User import Appointment, Salon, Service, User
from flask import Flask, request, jsonify
import json
from datetime import datetime, timedelta
import os
from PIL import Image


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
        service = Service.query.filter_by(id=int(appointment.service_id)).first()
        serialized_appointments.append({
            'salon_name': salon.name,
            'salon_street':salon.street,
            'service_name': service.name,
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
            if datetime.now() <= (appointment.datetime - timedelta(days=1)):
                db.session.delete(appointment)
                db.session.commit()
                return jsonify({'message': 'Запис успішно видалено'})
            else:
                return jsonify({'message': 'Запис можна скасувати не пізніше, ніж за добу'})
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
            service = Service.query.get(appointment.service_id)
            appointments_data.append({
                'user_name': user.name,
                'user_phone': user.phone,
                'salon_name': salon.name,
                'service_name': service.name,
                'datetime': appointment.datetime.strftime('%Y-%m-%d %H:%M')
            })
        return jsonify({'appointments': appointments_data})

    except Exception as e:
        return jsonify({'error': str(e)})