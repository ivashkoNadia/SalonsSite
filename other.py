from Entity.User import Service
from flask import Flask, request, jsonify

def fun_getservices(salon_id):
    services = Service.query.filter_by(salon_id=int(salon_id)).all()
    # Сформувати список словників із назвами послуг і цінами
    services_list = []
    for service in services:
        service_dict = {
            "id": service.id,
            "name": service.name,
            "price": service.price
        }
        services_list.append(service_dict)
    # Повернути список послуг у вигляді JSON
    return jsonify({"services": services_list})

def fun_editservices(salon_id, db, request):
    Service.query.filter_by(salon_id=salon_id).delete()
    db.session.commit()

    # Отримуємо нові дані про послуги з запиту
    procedures = request.form.getlist('procedures[]')
    prices = request.form.getlist('prices[]')
    # ids = request.form.getlist('id[]')

    # Вставляємо нові дані про послуги для вказаного салону
    for procedure, price in zip(procedures, prices):
        service = Service(salon_id=salon_id, name=procedure, price=price)
        db.session.add(service)
    db.session.commit()

    return jsonify({"message": "Список процедур оновлено успішно"})