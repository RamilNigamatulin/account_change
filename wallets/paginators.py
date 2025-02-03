from rest_framework.pagination import PageNumberPagination


class WalletsPaginator(PageNumberPagination):
    """Вывод списка до 10 кошельков или операций."""

    page_size = 10
    page_query_param = "page_size"
    max_page_size = 100
