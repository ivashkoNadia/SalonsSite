import Connection.main_data as main_data
from Entity.User import User
from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
import ssl


def send_email(recipient_email, message_text):
    subject= "Відновлення паролю"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(main_data.SENDER_EMAIL, main_data.SENDER_EMAIL_PASSWORD)

        message = MIMEText(message_text, _charset='utf-8')
        message["From"] = main_data.SENDER_EMAIL
        message["To"] = recipient_email
        message["Subject"] = subject

        server.sendmail(main_data.SENDER_EMAIL, recipient_email, message.as_string())
        return "Email успішно надіслано!"



def fun_reset_passsword(data, db):
    message=""
    try:
        user_email = data.get('user_email')

        # Перевірка чи існує такий email в таблиці User
        user = User.query.filter_by(email=user_email).first()

        if not user:
            return jsonify({'message': 'Користувача з такою електронною поштою не знайдено'})

        # Отримуємо поточний пароль і зсуваємо кожен символ на 3 значення
        original_password = user.password
        new_password = ''.join(chr((ord(char) + 3 - 32) % 95 + 32) for char in original_password)

        text= "Ваш новий пароль для входу у акаунт: "+new_password + '\n' + "За потреби можете потім змінити пароль в налаштуваннях акаунту"

        try:
            send_email(user_email, text)
            # Оновлення паролю в базі даних
            user.password = new_password
            db.session.commit()
            message = {'message': 'Новий пароль відправлено на вашу електронну пошту'}
        except Exception as e:
            message = {'message': f'Не вдалося відправити лист: {str(e)}'}


    except Exception as e:
        message = {'message': str(e)}
    return message


