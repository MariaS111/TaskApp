from django.core.mail import EmailMessage, send_mass_mail
from TaskApp import settings
from users.models import CustomUser


class Util:
    @staticmethod
    def send_verification_email(data):
        email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=(data['to_email'],))
        email.send()

    @staticmethod
    def send_email():
        users = CustomUser.objects.all()
        message_data = [('Hello from your Task App', 'Your tasks are waiting for you here!',  "admin@example.com", [user.email]) for user in users]
        send_mass_mail(message_data, fail_silently=False)

