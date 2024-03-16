from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from apps.users.models import CustomUser
from django.conf import settings
from celery import shared_task

@shared_task
def send_verification_email(email):
    generated_code = get_random_string(length=6, allowed_chars='0123456789')
    user = CustomUser.objects.get(email=email)
    user.code = generated_code
    user.save()
    subject = 'Your verification code'
    massage = f'Your verification code:\n{generated_code}'
    from_mail = settings.EMAIL_HOST_USER
    send_mail(subject, massage, from_mail, [email])

@shared_task
def spam_email():
    from_mail = settings.EMAIL_HOST_USER
    send_mail(subject='Hhahaha', message='Hello brother!!', from_email=from_mail, recipient_list=['bekbolsuntk@gmail.com'])