import smtplib
from email.message import EmailMessage
from database import get_db
from database.models import *

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "ejes4tsay@gmail.com"
EMAIL_PASSWORD = "uzyymavcglhnyhzx"

def send_email_notification(task_data, user_id):
    db = next(get_db())
    recipient_email_obj = db.query(User).filter_by(id=user_id).first()
    if recipient_email_obj is None:
        print("Пользователь не найден.")
        return False
    recipient_email = recipient_email_obj.email
    msg = EmailMessage()
    msg['Subject'] = f"Новая задача: {task_data['title']}"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email
    task_info = f"""
    <h3>🔔 Вам назначена новая задача!</h3>
    <ul>
        <li><strong>Название:</strong> {task_data['title']}</li>
        <li><strong>Описание:</strong> {task_data.get('description', 'Не указано')}</li>
        <li><strong>Срок выполнения:</strong> {task_data.get('due_date', 'Не установлен')}</li>
        <li><strong>Статус:</strong> {'Выполнено' if task_data.get('completed') else 'Не выполнено'}</li>
    </ul>
    """
    msg.set_content(task_info, subtype='html')
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"Уведомление отправлено на {recipient_email}")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"Ошибка аутентификации при отправке письма: {e}")
        return False
    except smtplib.SMTPConnectError as e:
        print(f"Ошибка подключения к SMTP серверу: {e}")
        return False
    except smtplib.SMTPException as e:
        print(f"Ошибка при отправке письма: {e}")
        return False
    except Exception as e:
        print(f"Неизвестная ошибка при отправке письма: {e}")
        return False
