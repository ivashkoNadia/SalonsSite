from Entity.User import Appointment, Salon, Service
from flask import Flask, request, jsonify
import json
import io

from PIL import Image
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


