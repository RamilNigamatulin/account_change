from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
)
from rest_framework.response import Response

from wallets.models import Wallet, Operation
from wallets.paginators import WalletsPaginator
from wallets.permissions import IsAuthorOrSuperuser
from wallets.serializers import (
    WalletSerializer,
    OperationSerializer,
    WalletDetailSerializer,
)
from wallets.tasks import create_operation


class WalletCreateAPIView(CreateAPIView):
    """Создаем кошелек."""

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def perform_create(self, serializer):
        """Устанавливаем кошелек пользователя."""
        serializer.save(user=self.request.user)


class WalletListAPIView(ListAPIView):
    """Получаем кошельки только текущего пользователя."""

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    pagination_class = WalletsPaginator

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Wallet.objects.all()
        return Wallet.objects.filter(user=user)


class WalletRetrieveAPIView(RetrieveAPIView):
    """Получаем кошелек по UUID."""

    queryset = Wallet.objects.all()
    serializer_class = WalletDetailSerializer
    lookup_field = "uuid"
    permission_classes = [
        IsAuthorOrSuperuser,
    ]


class WalletDeleteAPIView(DestroyAPIView):
    """Удаляем кошелек."""

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = "uuid"
    permission_classes = [
        IsAuthorOrSuperuser,
    ]


class OperationListAPIView(ListAPIView):
    """Получаем операции только для текущего кошелька."""

    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    pagination_class = WalletsPaginator

    def get_queryset(self):
        wallet_uuid = self.kwargs.get("uuid")
        user = self.request.user
        if not wallet_uuid:
            return Operation.objects.none()
        if user.is_superuser:
            return Operation.objects.filter(wallet__uuid=wallet_uuid)

        return Operation.objects.filter(wallet__uuid=wallet_uuid, wallet__user=user)


class OperationCreateAPIView(CreateAPIView):
    """Создаем операцию."""

    queryset = Operation.objects.all()
    serializer_class = OperationSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Создаем операцию с обработкой ошибок."""

        wallet_uuid = self.kwargs.get("uuid")
        user = request.user
        try:
            wallet = Wallet.objects.select_for_update().get(uuid=wallet_uuid, user=user)
        except ObjectDoesNotExist:
            return Response(
                {
                    "error": "Кошелек не найден или не принадлежит текущему пользователю."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            operation_type = request.data.get("operation_type")
            amount = Decimal(request.data.get("amount", 0))
        except (TypeError, ValueError):
            return Response(
                {
                    "error": "Невалидные данные. Убедитесь, что переданы корректные тип операции и сумма."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if amount <= 0:
            return Response(
                {"error": "Сумма должна быть положительной."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if operation_type not in [
            Operation.Operations.DEPOSIT,
            Operation.Operations.WITHDRAWAL,
        ]:
            return Response(
                {
                    "error": "Неверный тип операции. Допустимые значения: DEPOSIT, WITHDRAWAL."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if (
            operation_type == Operation.Operations.WITHDRAWAL
            and wallet.balance < amount
        ):
            return Response(
                {"error": "Недостаточно средств на кошельке."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        create_operation.delay(wallet_uuid, operation_type, amount, user.id)

        return Response(
            {"message": "Операция успешно создана и будет обработана."},
            status=status.HTTP_201_CREATED,
        )
