from drf_spectacular.utils import extend_schema
from .serializers import (
    TourOperatorSerializer,
    GalleryTourSerializer,
    AvailableDateTourSerializer,
    OrderSerializer,
    TourCreateUpdateSerializer,
    TourDetailSerializer
)


from .serializers import TourDetailSerializer, TourCreateUpdateSerializer
from .models import Tour

class TourSwagger:
    """Документация для API туров."""

    tour_list = extend_schema(
        methods=["GET"],
        summary="📋 Список туров",
        description="Возвращает список всех туров с подробностями (теги и изображения).",
        responses={200: TourDetailSerializer(many=True)},
    )

    tour_create = extend_schema(
        methods=["POST"],
        summary="Добавить тур",
        description="Создаёт новый тур, включая теги и изображения.",
        request=TourCreateUpdateSerializer,
        responses={
            201: TourDetailSerializer,
            400: "Ошибка в данных",
        },
    )

    tour_retrieve = extend_schema(
        methods=["GET"],
        summary="🔍 Тур по ID",
        description="Получает данные о туре по его ID, включая теги и изображения.",
        responses={200: TourDetailSerializer, 404: "Не найдено"},
    )

    tour_update = extend_schema(
        methods=["PUT", "PATCH"],
        summary="✏️ Обновить тур",
        description="Обновляет данные тура. Можно использовать `PUT` или `PATCH`.",
        request=TourCreateUpdateSerializer,
        responses={
            200: TourDetailSerializer,
            400: "Ошибка в данных",
            404: "Не найдено",
        },
    )

    tour_delete = extend_schema(
        methods=["DELETE"],
        summary="🗑️ Удалить тур",
        description="Удаляет тур по его ID.",
        responses={204: None, 404: "Не найдено"},
    )



from .serializers import OrderSerializer
from .models import Order

class OrderSwagger:
    """Документация для API заказов туров."""

    order_list = extend_schema(
        methods=["GET"],
        summary="📋 Список заказов",
        description="Возвращает список всех заказов туров.",
        responses={200: OrderSerializer(many=True)},
    )

    order_create = extend_schema(
        methods=["POST"],
        summary="Добавить заказ",
        description="Создаёт новый заказ на тур.",
        request=OrderSerializer,
        responses={
            201: OrderSerializer,
            400: "Ошибка в данных",
        },
    )

    order_detail = extend_schema(
        methods=["GET"],
        summary="🔍 Заказ по ID",
        description="Получает данные о заказе по его ID.",
        responses={200: OrderSerializer, 404: "Не найдено"},
    )

    order_update = extend_schema(
        methods=["PUT", "PATCH"],
        summary="✏️ Обновить заказ",
        description="Обновляет данные заказа. Можно использовать `PUT` или `PATCH`.",
        request=OrderSerializer,
        responses={
            200: OrderSerializer,
            400: "Ошибка в данных",
            404: "Не найдено",
        },
    )

    order_delete = extend_schema(
        methods=["DELETE"],
        summary="🗑️ Удалить заказ",
        description="Удаляет заказ по его ID.",
        responses={204: None, 404: "Не найдено"},
    )

from drf_spectacular.utils import extend_schema
from .serializers import AvailableDateTourSerializer
from .models import AvailableDateTour

class AvailableDateTourSwagger:
    """Документация для API доступных дат туров."""

    available_date_tour_list = extend_schema(
        methods=["GET"],
        summary="📋 Список доступных дат туров",
        description="Возвращает список всех доступных дат для туров.",
        responses={200: AvailableDateTourSerializer(many=True)},
    )

    available_date_tour_create = extend_schema(
        methods=["POST"],
        summary="Добавить доступную дату тура",
        description="Создаёт новую доступную дату для тура.",
        request=AvailableDateTourSerializer,
        responses={
            201: AvailableDateTourSerializer,
            400: "Ошибка в данных",
        },
    )

    available_date_tour_detail = extend_schema(
        methods=["GET"],
        summary="🔍 Доступная дата по ID",
        description="Получает информацию о доступной дате тура по ID.",
        responses={200: AvailableDateTourSerializer, 404: "Не найдено"},
    )

    available_date_tour_update = extend_schema(
        methods=["PUT", "PATCH"],
        summary="✏️ Обновить доступную дату тура",
        description="Обновляет данные о доступной дате для тура. Можно использовать `PUT` или `PATCH`.",
        request=AvailableDateTourSerializer,
        responses={
            200: AvailableDateTourSerializer,
            400: "Ошибка в данных",
            404: "Не найдено",
        },
    )

    available_date_tour_delete = extend_schema(
        methods=["DELETE"],
        summary="🗑️ Удалить доступную дату тура",
        description="Удаляет доступную дату для тура по ID.",
        responses={204: None, 404: "Не найдено"},
    )
from drf_spectacular.utils import extend_schema
from .serializers import GalleryTourSerializer
from .models import GalleryTour

class GalleryTourSwagger:
    """Документация для API галерей туров."""

    gallery_tour_list = extend_schema(
        methods=["GET"],
        summary="📋 Список галерей туров",
        description="Возвращает список всех фотографий для туров.",
        responses={200: GalleryTourSerializer(many=True)},
    )

    gallery_tour_create = extend_schema(
        methods=["POST"],
        summary="Добавить изображение в галерею тура",
        description="Создаёт новое изображение для галереи указанного тура.",
        request=GalleryTourSerializer,
        responses={
            201: GalleryTourSerializer,
            400: "Ошибка в данных",
        },
    )

    gallery_tour_detail = extend_schema(
        methods=["GET"],
        summary="🔍 Изображение галереи по ID",
        description="Получает информацию о фотографии в галерее тура по ID.",
        responses={200: GalleryTourSerializer, 404: "Не найдено"},
    )

    gallery_tour_update = extend_schema(
        methods=["PUT", "PATCH"],
        summary="✏️ Обновить изображение в галерее тура",
        description="Обновляет изображение галереи тура. Можно использовать `PUT` или `PATCH`.",
        request=GalleryTourSerializer,
        responses={
            200: GalleryTourSerializer,
            400: "Ошибка в данных",
            404: "Не найдено",
        },
    )

    gallery_tour_delete = extend_schema(
        methods=["DELETE"],
        summary="🗑️ Удалить изображение из галереи тура",
        description="Удаляет изображение из галереи по ID.",
        responses={204: None, 404: "Не найдено"},
    )



from .serializers import TourOperatorSerializer
from .models import TourOperator

class TourOperatorSwagger:
    """Документация для API туроператоров."""

    tour_operator_list = extend_schema(
        methods=["GET"],
        summary="📋 Список туроператоров",
        description="Возвращает список всех туроператоров.",
        responses={200: TourOperatorSerializer(many=True)},
    )

    tour_operator_create = extend_schema(
        methods=["POST"],
        summary="Добавить туроператора",
        description="Создаёт нового туроператора.",
        request=TourOperatorSerializer,
        responses={
            201: TourOperatorSerializer,
            400: "Ошибка в данных",
        },
    )

    tour_operator_detail = extend_schema(
        methods=["GET"],
        summary="🔍 Туроператор по ID",
        description="Получает информацию о туроператоре по ID.",
        responses={200: TourOperatorSerializer, 404: "Не найдено"},
    )

    tour_operator_update = extend_schema(
        methods=["PUT", "PATCH"],
        summary="✏️ Обновить туроператора",
        description="Обновляет данные туроператора. Можно использовать `PUT` или `PATCH`.",
        request=TourOperatorSerializer,
        responses={
            200: TourOperatorSerializer,
            400: "Ошибка в данных",
            404: "Не найдено",
        },
    )

    tour_operator_delete = extend_schema(
        methods=["DELETE"],
        summary="🗑️ Удалить туроператора",
        description="Удаляет туроператора по ID.",
        responses={204: None, 404: "Не найдено"},
    )

from drf_spectacular.utils import extend_schema
from .serializers import TagSerializer

class TagSwagger:
    """Документация для API тегов."""

    list = extend_schema(
        methods=["GET"],
        summary="📋 Список тегов",
        description="Возвращает список всех доступных тегов.",
        responses={200: TagSerializer(many=True)},
    )

    create = extend_schema(
        methods=["POST"],
        summary="➕ Создать тег",
        description="Создаёт новый тег.",
        request=TagSerializer,
        responses={201: TagSerializer, 400: "Ошибка"},
    )

    retrieve = extend_schema(
        methods=["GET"],
        summary="🔍 Получить тег по ID",
        description="Получает данные тега по его ID.",
        responses={200: TagSerializer, 404: "Не найдено"},
    )

    update = extend_schema(
        methods=["PUT", "PATCH"],
        summary="✏️ Обновить тег",
        description="Обновляет существующий тег по ID. Поддерживает PUT и PATCH.",
        request=TagSerializer,
        responses={200: TagSerializer, 400: "Ошибка", 404: "Не найдено"},
    )

    destroy = extend_schema(
        methods=["DELETE"],
        summary="🗑️ Удалить тег",
        description="Удаляет тег по его ID.",
        responses={204: None, 404: "Не найдено"},
    )
