from rest_framework.serializers import ModelSerializer

from wallets.models import Wallet, Operation


class WalletSerializer(ModelSerializer):
    """Сериализатор для кошелька."""

    class Meta:
        model = Wallet
        fields = "__all__"
        read_only_fields = ["uuid"]


class OperationSerializer(ModelSerializer):
    """Сериализатор для операции."""

    class Meta:
        model = Operation
        fields = "__all__"


class WalletDetailSerializer(ModelSerializer):
    """Сериализатор для детального представления кошелька с добавлением операций."""

    operations = OperationSerializer(many=True, read_only="operations")

    class Meta:
        model = Wallet
        fields = [
            "user",
            "uuid",
            "balance",
            "created_at",
            "updated_at",
            "operations",
        ]
