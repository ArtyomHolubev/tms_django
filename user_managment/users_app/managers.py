from django.contrib.auth.models import BaseUserManager
from django.core.mail import send_mail


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        send_mail(
            from_email="aliaksei.kudrautsau@gmail.com",
            message="Your account is active",
            subject="Account active",
            recipient_list=[email]
        )

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)