from Entity.User import Feedback
from flask import Flask, request, jsonify


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