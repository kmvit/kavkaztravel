from drf_spectacular.utils import extend_schema
from .serializers import (
    TourOperatorSerializer,
    AttractionTourSerializer,
    ThemeTourSerializer,
    ParticipantTypeTourSerializer,
    FormatTourSerializer,
    DurationTourSerializer,
    SpecialOfferTourSerializer,
    GalleryTourSerializer,
    TourConditionsSerializer,
    AvailableDateTourSerializer,
    OrderSerializer,
    TourSerializer
)

class SimpleSwagger:
    """Базовый класс для Swagger-документации"""

    @classmethod
    def make(cls, serializer, create_serializer=None):
        return type(f"{serializer.__name__}Swagger", (cls,), {
            # Общие настройки для всех ViewSet
            "list": extend_schema(
                methods=["GET"],
                summary=f"📋 Список {serializer.Meta.model._meta.verbose_name_plural}",
                description=f"Получение списка {serializer.Meta.model._meta.verbose_name_plural}",
                responses={200: serializer(many=True)}
            ),

            "create": extend_schema(
                methods=["POST"],
                summary=f"➕ Создать {serializer.Meta.model._meta.verbose_name}",
                description=f"Создание нового {serializer.Meta.model._meta.verbose_name}",
                request=create_serializer or serializer,
                responses={
                    201: create_serializer or serializer,
                    400: "Ошибка валидации"
                }
            ),

            "retrieve": extend_schema(
                methods=["GET"],
                summary=f"🔍 Детали {serializer.Meta.model._meta.verbose_name}",
                description=f"Получение детальной информации о {serializer.Meta.model._meta.verbose_name}",
                responses={
                    200: serializer,
                    404: "Не найдено"
                }
            ),

            "update": extend_schema(
                methods=["PUT", "PATCH"],
                summary=f"✏️ Обновить {serializer.Meta.model._meta.verbose_name}",
                description=f"Обновление данных {serializer.Meta.model._meta.verbose_name}",
                request=create_serializer or serializer,
                responses={
                    200: create_serializer or serializer,
                    400: "Ошибка валидации",
                    404: "Не найдено"
                }
            ),

            "destroy": extend_schema(
                methods=["DELETE"],
                summary=f"🗑️ Удалить {serializer.Meta.model._meta.verbose_name}",
                description=f"Удаление {serializer.Meta.model._meta.verbose_name}",
                responses={
                    204: "Успешное удаление",
                    404: "Не найдено"
                }
            )
        })


# Генерация Swagger-классов
TourOperatorSwagger = SimpleSwagger.make(
    serializer=TourOperatorSerializer,
    create_serializer=TourOperatorSerializer  # Можно указать другой сериализатор для создания
)

AttractionTourSwagger = SimpleSwagger.make(
    serializer=AttractionTourSerializer
)

# Добавляем новые классы документации
ParticipantTypeTourSwagger = SimpleSwagger.make(
    serializer=ParticipantTypeTourSerializer
)

FormatTourSwagger = SimpleSwagger.make(
    serializer=FormatTourSerializer
)

DurationTourSwagger = SimpleSwagger.make(
    serializer=DurationTourSerializer
)

SpecialOfferTourSwagger = SimpleSwagger.make(
    serializer=SpecialOfferTourSerializer
)

GalleryTourSwagger = SimpleSwagger.make(
    serializer=GalleryTourSerializer
)


TourConditionsSwagger = SimpleSwagger.make(
    serializer=TourConditionsSerializer
)

AvailableDateTourSwagger = SimpleSwagger.make(
    serializer=AvailableDateTourSerializer
)

OrderSwagger = SimpleSwagger.make(
    serializer=OrderSerializer
)

TourSwagger = SimpleSwagger.make(
    serializer=TourSerializer
)

ThemeTourSwagger = SimpleSwagger.make(
    serializer= ThemeTourSerializer
)