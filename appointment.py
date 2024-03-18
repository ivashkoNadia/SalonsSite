from Entity.User import Appointment, Salon, Service
from flask import Flask, request, jsonify
import json
from datetime import datetime


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
            'datetime': appointment.datetime.strftime('%Y-%m-%d %H:%M')  # Перетворення в формат рядка
        })
    # Повертаємо серіалізовані дані у форматі JSON
    return jsonify({'appointments': serialized_appointments})