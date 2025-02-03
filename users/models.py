from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Создание модели пользователя."""

    username = None
    first_name = models.CharField(
        max_length=30,
        verbose_name="Имя пользователя",
        help_text="Введите имя пользователя",
        **NULLABLE,
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия пользователя",
        help_text="Введите фамилию пользователя",
        **NULLABLE,
    )
    phone = PhoneNumberField(
        verbose_name="Номер телефона",
        help_text="Введите номер телефона пользователя",
        **NULLABLE,
    )
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        help_text="Введите адрес электронной почты",
        unique=True,
    )
    image = models.ImageField(
        verbose_name="Изображение профиля",
        help_text="Загрузите изображение",
        upload_to="photo/users",
        **NULLABLE,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def _str__(self):
        return self.email
