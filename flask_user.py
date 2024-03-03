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
        errors["message"]="Користувач успішно зареєстрований"

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





if __name__ == '__main__':
    app.run(debug=True)




#
# @app.route('/get_user/<email>')
# def get_user(email):
#     user = u.User.query.filter_by(email=email).first()
#     if user:
#         return f"User found: {user.name}, {user.email}, {user.type_user}"
#     else:
#         return "User not found"

