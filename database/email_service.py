import smtplib
from email.message import EmailMessage

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "nrvnqsr.049@gmail.com"
EMAIL_PASSWORD = ""

def send_email_notification(recipient_email: str, task: dict):
    msg = EmailMessage()
    msg['Subject'] = f"Новая задача: {task['title']}"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email

    task_info = f"""
    <h3>🔔 Вам назначена новая задача!</h3>
    <ul>
        <li><strong>Название:</strong> {task['title']}</li>
        <li><strong>Описание:</strong> {task.get('description', 'Не указано')}</li>
        <li><strong>Срок выполнения:</strong> {task.get('due_date', 'Не установлен')}</li>
        <li><strong>Статус:</strong> {'Выполнено' if task.get('completed') else 'Не выполнено'}</li>
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
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")
        return False
