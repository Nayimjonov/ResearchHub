from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from .models import User, UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def send_verification_email_on_create(sender, instance, created, **kwargs):
    if created and not instance.is_verified:
        if not instance.email_token:
            instance.email_token = get_random_string(32)
            instance.save(update_fields=['email_token'])

        message = (
            f"Здравствуйте, {instance.username}!\n\n"
            f"Вы зарегистрировались в нашем сервисе.\n"
            f"Для подтверждения электронной почты используйте следующий код подтверждения:\n\n"
            f"{instance.email_token}\n\n"
            f"Если вы не регистрировались на нашем сайте, просто проигнорируйте это письмо."
        )

        send_mail(
            subject='Подтверждение электронной почты',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=False,
        )
