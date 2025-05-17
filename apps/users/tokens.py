# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import send_mail
# from rest_framework.exceptions import ValidationError
# from .models import User
#
#
# def generate_reset_token(user):
#     return default_token_generator.make_token(user)
#
#
# def send_password_reset_email(user):
#     token = generate_reset_token(user)
#     subject = "Сброс пароля"
#     from_email = "support@yourdomain.com"
#     to_email = [user.email]
#
#     message = (
#         f"Здравствуйте, {user.first_name}!\n\n"
#         f"Вы запросили сброс пароля.\n"
#         f"Ваш токен для сброса пароля:\n\n{token}\n\n"
#         f"Если вы не запрашивали сброс пароля, проигнорируйте это письмо.\n\n"
#         f"С уважением,\nКоманда поддержки"
#     )
#
#     send_mail(subject, message, from_email, [to_email])
#
#
# def reset_password_confirm(data):
#     token = data.get('token')
#     password = data.get('password')
#     password_confirm = data.get('password_confirm')
#
#     if not token or not password or not password_confirm:
#         raise ValidationError("Все поля обязательны: token, password, password_confirm.")
#
#     if password != password_confirm:
#         raise ValidationError("Пароли не совпадают.")
#
#     user = next((u for u in User.objects.iterator() if default_token_generator.check_token(u, token)), None)
#     if not user:
#         raise ValidationError("Токен недействителен или истёк срок его действия.")
#
#     user.set_password(password)
#     user.save()
#     return {"detail": "Пароль успешно обновлён."}
