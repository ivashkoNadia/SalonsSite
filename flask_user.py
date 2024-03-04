from flask import Flask, request, jsonify
from flask_cors import CORS
from Entity.User import db, User
import main_data

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = main_data.DB_CONNECTION
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


if __name__ == '__main__':
    app.run(debug=True)


