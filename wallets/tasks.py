from celery import shared_task
from django.db import transaction
from wallets.models import Wallet, Operation


@shared_task
def create_operation(wallet_uuid, operation_type, amount, user_id):
    """Асинхронная задача для обработки операции."""

    with transaction.atomic():
        wallet = Wallet.objects.get(uuid=wallet_uuid, user_id=user_id)

        if operation_type == Operation.Operations.DEPOSIT:
            wallet.balance += amount
        elif operation_type == Operation.Operations.WITHDRAWAL:
            wallet.balance -= amount

        wallet.save()
        operation = Operation.objects.create(
            wallet=wallet, operation_type=operation_type, amount=amount
        )

    return operation.id
