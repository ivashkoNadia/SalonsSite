from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import salon
import other
import feedback
import appointment
import user
from Entity.User import db
import Connection.main_data as main_data

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = main_data.DB_CONNECTION
db.init_app(app)

@app.route('/add_user', methods=['POST'])
def add_user():
    return user.fun_add_user(request.get_json())

@app.route('/login', methods=['POST'])
def login_user():
    return user.fun_login_user(request.get_json())


# @app.route('/get_our_user', methods=['GET'])
# def get_our_user():
#     data = request.get_json()
#     user_id = data.get('user_id')  # Отримуємо id користувача для редагування
#     user = User.query.filter_by(user_id=user_id).first()
#     print(user.name)
#     return jsonify({
#         'user_id': user.user_id,
#         'name': user.name,
#         'email': user.email,
#         'type_user': user.type_user,
#         'phone': user.phone
#     })


@app.route('/edit_user', methods=['POST'])
def edit_user():
    return user.fun_edit_user(request.get_json(), db)

@app.route('/edit_user_password', methods=['POST'])
def edit_user_password():
    return user.fun_edit_user_password(request.get_json(), db)

@app.route('/available_salons', methods=['GET'])
def get_salons_availavle():
    return salon.fun_salons_availavle()

@app.route('/salon_details', methods=['POST'])
def salon_details():
    return salon.fun_salon_details(request.get_json(), db)

@app.route('/salon_services', methods=['POST'])
def salon_services():
    return salon.fun_salon_services(request.get_json())

@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    return appointment.fun_add_appointment(request.get_json())

@app.route('/add_feedback', methods=['POST'])
def add_feedback():
    return feedback.fun_add_feedback(request.get_json(), db)

@app.route('/salon_feedback', methods=['POST'])
def salon_feedback():
    return feedback.fun_feedback(request.get_json())

@app.route('/user_appointments', methods=['POST'])
def user_appointments():
    return appointment.fun_user_appointments(request.get_json())

@app.route('/delete_appointment/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    return appointment.fun_delete_appointment(appointment_id, db)

@app.route('/client_appointments', methods=['POST'])
def get_user_appointments():
    return appointment.fun_client_appointments(request.get_json())

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    return salon.fun_photo(request, db)

@app.route('/salon_approve', methods=['GET'])
def get_unapproved_salons():
    return salon.fun_approve_salon()

@app.route('/approve_salon/<int:salon_id>', methods=['POST'])
def approve_salon(salon_id):
    return salon.fun_really_approve(salon_id, db)

@app.route('/delete_salon/<int:salon_id>', methods=['DELETE'])
def delete_salon(salon_id):
    return salon.fun_delete_salon(salon_id, db)

@app.route("/services/<int:salon_id>", methods=["GET"])
def get_services_by_salon_id(salon_id):
    return other.fun_getservices(salon_id)

@app.route("/edit_services/<int:salon_id>", methods=["POST"])
def update_services(salon_id):
    return other.fun_editservices(salon_id, db, request)

if __name__ == '__main__':
    app.run(debug=True)


