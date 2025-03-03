from rest_framework.pagination import PageNumberPagination


class ReviewPagination(PageNumberPagination):
    page_size = 5  # Количество отзывов на одной странице
    page_size_query_param = (
        "page_size"  # Позволяет клиенту менять размер страницы через ?page_size=10
    )
    max_page_size = 50  # Максимальное количество отзывов на странице
