import random
import string
import requests

from datetime import timedelta
from django.utils import timezone
from django.conf import settings

from .models import SMSVerification


def generate_code(length=6):
    """Генерация случайного кода из цифр."""
    return "".join(random.choices(string.digits, k=length))


def send_sms(phone_number, code):
    """Отправка SMS через API SMS.ru с кодом подтверждения."""
    url = "https://sms.ru/sms/send"

    params = {
        "api_id": settings.SMS_API_KEY,  # API ключ
        "to": phone_number,  # Номер получателя
        "msg": f"Ваш код подтверждения: {code}",  # Сообщение с кодом
        "json": 1,  # Ответ в формате JSON
    }

    try:
        response = requests.post(url, data=params)
        response.raise_for_status()  # Поднимет исключение, если HTTP-статус 4xx или 5xx

        try:
            response_json = response.json()
        except ValueError:
            raise Exception(f"Ошибка при обработке ответа от API: {response.text}")

        # Логируем весь ответ для отладки
        print("Ответ от API:", response_json)

        # Проверяем, что в ответе есть нужный ключ для номера телефона
        if "sms" in response_json and phone_number in response_json["sms"]:
            sms_info = response_json["sms"][phone_number]
            if "sms_id" in sms_info:
                # Возвращаем 'sms_id' из ответа
                return sms_info["sms_id"]
            else:
                raise Exception(
                    f"Ошибка при отправке SMS: отсутствует 'sms_id' для номера {phone_number}. Ответ: {response_json}"
                )
        else:
            raise Exception(
                f"Ошибка: данные по номеру {phone_number} отсутствуют в ответе. Ответ: {response_json}"
            )

    except requests.exceptions.RequestException as e:
        raise Exception(f"Ошибка при отправке SMS: {str(e)}")


def send_verification_sms(phone_number):
    """Генерация кода и отправка SMS."""
    code = generate_code()  # Генерируем случайный код
    try:
        # Получаем 'sms_id' из ответа
        message_id = send_sms(phone_number, code)

        # Создаем запись в базе данных с кодом, временем истечения и статусом
        expires_at = timezone.now() + timedelta(
            minutes=5
        )  # Код будет действителен 5 минут
        verification = SMSVerification.objects.create(
            phone_number=phone_number,
            verification_code=code,
            message_id=message_id,
            status="sent",
            expires_at=expires_at,
        )

        return verification
    except Exception as e:
        print(f"Ошибка при отправке SMS или сохранении в базе: {e}")
        raise


from django.core.mail import send_mail

def send_notification_email(user, message):
    send_mail(
        'Новое уведомление',  # Тема письма
        message,  # Текст уведомления
        'from@example.com',  # Адрес отправителя
        [user.email],  # Адрес получателя
        fail_silently=False,
    )
