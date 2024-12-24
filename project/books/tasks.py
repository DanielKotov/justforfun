from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_registration_email(user_email):
    subject = "Регистрация на сервисе"
    message = "Вы зарегистрировались на сервисе."
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)

@shared_task
def send_book_creation_email(user_email, book_title):
    subject = "Создание книги"
    message = f"Вы создали книгу с названием: {book_title}"
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)
