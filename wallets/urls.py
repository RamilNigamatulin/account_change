from django.urls import path

from wallets.apps import WalletsConfig
from wallets.views import (
    WalletCreateAPIView,
    WalletListAPIView,
    WalletDeleteAPIView,
    WalletRetrieveAPIView,
    OperationCreateAPIView,
    OperationListAPIView,
)

app_name = WalletsConfig.name

urlpatterns = [
    path("", WalletListAPIView.as_view(), name="list-wallets"),
    path("create/", WalletCreateAPIView.as_view(), name="create-wallets"),
    path("<uuid:uuid>/", WalletRetrieveAPIView.as_view(), name="retrieve-wallets"),
    path(
        "<uuid:uuid>/delete/",
        WalletDeleteAPIView.as_view(),
        name="delete-wallets",
    ),
    path(
        "operations/<uuid:uuid>/",
        OperationListAPIView.as_view(),
        name="list-operations",
    ),
    path(
        "<uuid:uuid>/operations/",
        OperationCreateAPIView.as_view(),
        name="create-operations",
    ),
]
