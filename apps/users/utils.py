from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from apps.users.models import CustomUser
from django.conf import settings

def send_verification_email(email):
    generated_code = get_random_string(length=6, allowed_chars='0123456789')
    user = CustomUser.objects.get(email=email)
    user.code = generated_code
    user.save()
    subject = 'Your verification code'
    massage = f'Your verification code:\n{generated_code}'
    from_mail = settings.EMAIL_HOST_USER
    send_mail(subject, massage, from_mail, [email])