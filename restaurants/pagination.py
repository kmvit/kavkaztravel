from rest_framework.pagination import PageNumberPagination


class ReviewPagination(PageNumberPagination):
    """
    Класс пагинации для отзывов.

    Настраивает количество объектов на странице, позволяя задавать размер страницы через параметр 'page_size'
    и ограничивая максимальное количество объектов на странице до 50.
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 50
