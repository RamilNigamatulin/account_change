from django.contrib import admin

from wallets.models import Wallet, Operation


@admin.register(Wallet)
class Wallet(admin.ModelAdmin):
    """Модель административного интерфейса для кошелька."""

    list_display = (
        "user",
        "balance",
        "created_at",
    )
    list_filter = (
        "user",
        "balance",
        "created_at",
        "updated_at",
    )
    search_fields = ("user",)


@admin.register(Operation)
class Operation(admin.ModelAdmin):
    """Модель административного интерфейса для операции."""

    list_display = (
        "wallet",
        "operation_type",
        "amount",
        "created_at",
    )
    list_filter = (
        "wallet",
        "operation_type",
        "amount",
        "created_at",
    )
