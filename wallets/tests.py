from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from wallets.models import Wallet, Operation


class WalletTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru")
        self.wallet = Wallet.objects.create(user=self.user)
        self.operation = Operation.objects.create(
            operation_type="DEPOSIT", wallet=self.wallet, amount=1.01
        )
        self.client.force_authenticate(user=self.user)

    def test_wallet_retrieve(self):
        url = reverse("wallets:retrieve-wallets", args=(self.wallet.uuid,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("uuid"), str(self.wallet.uuid))

    def test_wallet_create(self):
        url = reverse("wallets:create-wallets")
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wallet.objects.all().count(), 2)

    def test_wallet_delete(self):
        url = reverse("wallets:delete-wallets", args=(self.wallet.uuid,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Wallet.objects.all().count(), 0)

    def test_wallet_list(self):
        url = reverse("wallets:list-wallets")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "uuid": str(self.wallet.uuid),
                    "balance": f"{self.wallet.balance:.2f}",
                    "created_at": self.wallet.created_at.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    "updated_at": self.wallet.updated_at.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    "user": self.wallet.user.id,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class OperationTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru")
        self.wallet = Wallet.objects.create(user=self.user)
        self.operation = Operation.objects.create(
            operation_type="DEPOSIT", wallet=self.wallet, amount=1.01
        )
        self.client.force_authenticate(user=self.user)

    def test_operation_create(self):
        url = reverse("wallets:create-operations", args=[self.wallet.uuid])
        data = {"operation_type": "DEPOSIT", "amount": 2.02}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Operation.objects.all().count(), 1)

    def test_operation_list(self):
        url = reverse("wallets:list-operations", args=[self.wallet.uuid])
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.operation.pk,
                    "operation_type": self.operation.operation_type,
                    "amount": f"{self.operation.amount:.2f}",
                    "created_at": self.operation.created_at.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    "wallet": str(self.wallet.uuid),
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
