from Entity.Appointment import Appointment
from Entity.Service import Service
from Entity.Salons import Salon
from flask import Flask, request, jsonify
import json
import io
import base64
from PIL import Image

def fun_salons_availavle():
    salons = Salon.query.filter_by(approve=1).all()

    salon_data = [{'id': salon.id, 'district': salon.district, 'name': salon.name, 'rating': salon.rating,
                   'owner_id': salon.owner_id,
                   'photo': base64.b64encode(salon.photo).decode('utf-8') if salon.photo else None} for salon in salons]

    return jsonify({'salons': salon_data})

def fun_salon_details(data, db):
    salon_id = data.get('salon_id')
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

def fun_salon_services(data):
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
    return jsonify({'services': serialized_services})


def fun_photo(request_, db):
    photo = request_.files['photo']
    if photo:
        allowed_formats = ['png', 'jpg']
        if photo.filename.lower().split('.')[-1] not in allowed_formats:
            return jsonify({'message': 'Фото повинно бути у форматі .png або .jpg'})

        # Відкриваємо фото за допомогою Pillow
        img = Image.open(photo)

        # Знаходимо меншу сторону фото
        width, height = img.size
        min_side = min(width, height)

        # Вирівнюємо фото по центру та обрізаємо до квадратного розміру
        left = (width - min_side) / 2
        top = (height - min_side) / 2
        right = (width + min_side) / 2
        bottom = (height + min_side) / 2
        img = img.crop((left, top, right, bottom))

        img = img.convert('RGB')

        # Перетворюємо зображення у байтовий об'єкт
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='JPEG')
        img_byte_array = img_byte_array.getvalue()

        #отримуємо дані
        district = request_.form.get('district')
        name = request_.form.get('name')
        street = request_.form.get('street')
        social = request_.form.get('social')
        owner_id = request_.form.get('owner_id')
        user_id_dict = json.loads(owner_id)
        owner_id = user_id_dict['user_id']

        salon = Salon(district=district, name=name, street=street, social=social, photo=img_byte_array, owner_id=owner_id,
                      rating=5, rating_amount=1, approve=0)
        salon.save_to_db()

        salon_id = salon.id
        try:
            # Отримуємо дані з запиту
            procedures = request_.form.getlist('procedures[]')
            prices = request_.form.getlist('prices[]')

            # Перевіряємо, чи всі дані є
            if salon_id and procedures and prices:
                # Зберігаємо кожну пару процедура-ціна до бази даних
                for procedure, price in zip(procedures, prices):
                    service = Service(salon_id=salon_id, name=procedure, price=price)
                    db.session.add(service)

                # Зберігаємо зміни
                db.session.commit()

                return jsonify({'message': "Дані про салон надіслано.\nПісля затвердження адміністрацією сайту - з'явиться на ньому"})
            else:
                return jsonify({'message': 'Недостатньо даних для збереження послуг'})

        except Exception as e:
            return jsonify({'message': str(e)})

    else:
        return jsonify({'message':'Помилка: Фото не було завантажено'})

def fun_approve_salon():
    salons = Salon.query.filter_by(approve=0).all()

    salon_data = []
    for salon in salons:
        # Отримуємо список процедур для кожного салону
        services = Service.query.filter_by(salon_id=salon.id).all()
        # Створюємо словник для кожного салону
        salon_dict = {
            'id': salon.id,
            'district': salon.district,
            'street': salon.street,
            'name': salon.name,
            'owner_id': salon.owner_id,
            'social': salon.social,
            'photo': base64.b64encode(salon.photo).decode('utf-8') if salon.photo else None,
            'services': [{'name': service.name, 'price': service.price} for service in services]
        }
        # Додаємо словник салону до списку
        salon_data.append(salon_dict)

    # Повертаємо список салонів з їхніми процедурами у форматі JSON
    return jsonify({'salons': salon_data})

def fun_really_approve(salon_id, db):
    try:
        salon = Salon.query.get(salon_id)

        if salon:
            salon.approve = 1
            db.session.commit()
            return jsonify({'message': 'Салон успішно затверджено'})
        else:
            return jsonify({'message': 'Салон з вказаним id не знайдено'})
    except Exception as e:
        return jsonify({'message': str(e)})

def fun_delete_salon(salon_id, db):
    try:
        salon = Salon.query.get(salon_id)

        if salon:
            db.session.delete(salon)
            db.session.commit()
            return jsonify({'message': 'Салон успішно видалено'})
        else:
            return jsonify({'message': 'Салон з вказаним id не знайдено'})
    except Exception as e:
        return jsonify({'message': str(e)})