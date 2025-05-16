from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from .models import User


@receiver(post_save, sender=User)
def send_verification_email_on_create(sender, instance, created, **kwargs):
    if created and not instance.is_verified:
        instance.email_token = instance.email_token or get_random_string(32)
        instance.save()

        message = (
            "Пожалуйста, подтвердите вашу почту, используя этот токен:\n\n"
            f"{instance.email_token}"
        )

        send_mail(
            subject="Подтверждение электронной почты",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=False,
        )
