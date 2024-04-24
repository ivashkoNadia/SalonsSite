from Entity.Feedback import Feedback
from Entity.Salons import Salon
from flask import Flask, request, jsonify
import json
from datetime import datetime

def fun_add_feedback(data, db):
    user_id = data.get('user_id')
    text = data.get('text')
    rating = data.get('rating')
    salon_id = data.get('salon_id')

    user_id_dict = json.loads(user_id)
    user_id = user_id_dict['user_id']

    # Створення нового об'єкту Feedback
    new_feedback = Feedback(user_id=int(user_id), text=text, rating=int(rating), salon_id=int(salon_id),
                            datetime=datetime.now())

    salon = Salon.query.filter_by(id=int(salon_id)).first()
    rating_amount = salon.rating_amount
    star = salon.rating
    new_rating = (star * rating_amount + rating) / (rating_amount + 1)
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

def fun_feedback(data):
    salon_id = data.get('salon_id')

    # Отримання відгуків для вказаного salon_id
    feedback_records = Feedback.query.filter_by(salon_id=int(salon_id)).all()

    # Перевірка чи є відгуки для вказаного salon_id
    if not feedback_records:
        return jsonify({'message': 'No feedback found for the specified salon ID'})

    # Серіалізація відгуків
    serialized_feedback = []
    for feedback in feedback_records:
        serialized_feedback.append({
            'text': feedback.text,
            'datetime': feedback.datetime.strftime('%Y-%m-%d %H:%M:%S'),  # Перетворення в формат рядка
            'rating': feedback.rating
        })

    # Повернення серіалізованих відгуків
    return jsonify({'feedback': serialized_feedback})