from Entity.Service import Service
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

    procedures = request.form.getlist('procedures[]')
    prices = request.form.getlist('prices[]')
    ids = request.form.getlist('id[]')
    deletes = request.form.getlist('deletes[]')

    for service_id in deletes:
        if service_id != "undefined":
            service = Service.query.get(service_id)
            if service:
                db.session.delete(service)


    for procedure, price, service_id in zip(procedures, prices, ids):
        if  service_id == "undefined":
            # Якщо сервіс не існує, додаємо новий
            new_service = Service(salon_id=salon_id, name=procedure, price=price)
            db.session.add(new_service)

        else:
            service = Service.query.get(service_id)
            service.name = procedure
            service.price = price

        # Збереження змін у базі даних
    db.session.commit()

    return jsonify({"message": "Список процедур оновлено успішно"})