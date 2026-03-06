# Файл для хранения глобального состояния приложения
# Этот файл используется для синхронизации между main.py и scheduler.py

"""
Глобальное состояние приложения
email_sending_enabled: True - отправка включена, False - отправка отключена
"""
email_sending_enabled = True

def get_email_status():
    """Получить текущий статус отправки"""
    return email_sending_enabled

def set_email_status(status: bool):
    """Установить статус отправки"""
    global email_sending_enabled
    email_sending_enabled = status
    return email_sending_enabled