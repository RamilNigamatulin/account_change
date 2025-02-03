import uuid
from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Wallet(models.Model):
    """Создание модели кошелька."""

    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        help_text="Введите данные пользователя",
        on_delete=models.CASCADE,
        **NULLABLE,
    )
    uuid = models.UUIDField(
        verbose_name="UUID кошелька",
        help_text="Уникальный идентификатор кошелька",
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4,
    )
    balance = models.DecimalField(
        verbose_name="Баланс кошелька",
        max_digits=10,
        decimal_places=2,
        default=0.00,
        null=False,
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания кошелька",
        auto_now_add=True,
        help_text="Дата создания кошелька",
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата изменения кошелька",
        auto_now=True,
        help_text="Дата изменения кошелька",
    )

    class Meta:
        verbose_name = "Кошелек"
        verbose_name_plural = "Кошельки"
        ordering = [
            "uuid",
        ]

    def __str__(self):
        return f"Кошелек пользователя {self.user.email} с балансом {self.balance}"


class Operation(models.Model):
    """Создание модели операции."""

    class Operations(models.TextChoices):
        DEPOSIT = (
            "DEPOSIT",
            "Депозит",
        )
        WITHDRAWAL = (
            "WITHDRAWAL",
            "Вывод",
        )

    wallet = models.ForeignKey(
        Wallet,
        verbose_name="Кошелек",
        help_text="Введите кошелек",
        on_delete=models.CASCADE,
        related_name="operations",
        **NULLABLE,
    )
    operation_type = models.CharField(
        max_length=20,
        choices=Operations.choices,
        verbose_name="Тип операции",
        help_text="Выберете тип операции",
    )
    amount = models.DecimalField(
        verbose_name="Сумма операции",
        help_text="Укажите сумму операции",
        max_digits=10,
        decimal_places=2,
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания операции",
        auto_now_add=True,
        help_text="Дата создания операции",
    )

    class Meta:
        verbose_name = "Операция"
        verbose_name_plural = "Операции"

    def __str__(self):
        return f"Операция на кошельке {self.wallet.uuid}: {self.operation_type} на сумму {self.amount}"
