from drf_spectacular.utils import extend_schema
from .serializers import (
    CarSerializer,
    CarListSerializer,
    CarImageSerializer,
    RentalConditionSerializer,
    CarCreateUpdateSerializer,
    CarOptionSerializer,
    CarEquipmentSerializer,
    RentalDiscountSerializer,
    RentalSerializer,
)


class CarSwagger:
    """Документация для API автомобилей."""

    car_list = extend_schema(
        methods=["GET"],
        summary="📋 Список автомобилей",
        description="Возвращает список всех автомобилей.",
        responses={200: CarListSerializer(many=True)},
    )

    car_create = extend_schema(
        methods=["POST"],
        summary="Добавить автомобиль",
        description="Создаёт новый автомобиль.",
        request=CarCreateUpdateSerializer,
        responses={
            201: CarCreateUpdateSerializer,
            400: "Ошибка",
        },
    )

    car_detail = extend_schema(
        methods=["GET"],
        summary="🔍 Автомобиль получаемый по id",
        description="Получает данные об автомобиле по ID.",
        responses={200: CarSerializer, 404: "Не найдено"},
    )

    # Схема для обновления или частичного обновления автомобиля
    car_update = extend_schema(
        methods=["PUT", "PATCH"],  # Поддержка PUT и PATCH
        summary="✏️ Обновить автомобиль",  # Краткое описание
        description="Обновляет данные автомобиля. Можно использовать `PUT` или `PATCH`.",  # Подробное описание
        request=CarCreateUpdateSerializer,  # Сериализатор для тела запроса
        responses={  # Ожидаемые ответы
            200: CarCreateUpdateSerializer,  # Успешный ответ с обновленными данными
            400: "Ошибка",  # Ошибка в запросе
            404: "Не найдено",  # Если объект не найден
        },
    )

    car_delete = extend_schema(
        methods=["DELETE"],
        summary="🗑️ Удалить автомобиль",
        description="Удаляет автомобиль по ID.",
        responses={204: None, 404: "Не найдено"},
    )


class CarImageSwagger:
    """Документация для API изображений автомобилей."""

    image_list = extend_schema(
        methods=["GET"],
        summary="🖼️ Список изображений",
        description="Возвращает список всех изображений автомобилей.",
        responses={200: CarImageSerializer(many=True)},
    )

    image_create = extend_schema(
        methods=["POST"],
        summary="📷 Добавить изображение",
        description="Загружает новое изображение автомобиля.",
        request=CarImageSerializer,
        responses={201: CarImageSerializer, 400: "Ошибка"},
    )

    image_detail = extend_schema(
        methods=["GET"],
        summary="🔍 Детали изображения",
        description="Получает изображение автомобиля по ID.",
        responses={200: CarImageSerializer, 404: "Не найдено"},
    )

    image_delete = extend_schema(
        methods=["DELETE"],
        summary="❌ Удалить изображение",
        description="Удаляет изображение автомобиля по ID.",
        responses={204: None, 404: "Не найдено"},
    )


class RentalConditionSwagger:
    """Документация для API условий аренды."""

    rental_list = extend_schema(
        methods=["GET"],
        summary="📜 Список условий аренды",
        description="Возвращает список всех условий аренды.",
        responses={200: RentalConditionSerializer(many=True)},
    )

    rental_create = extend_schema(
        methods=["POST"],
        summary="📝 Добавить условия аренды",
        description="Создаёт новое условие аренды.",
        request=RentalConditionSerializer,
        responses={201: RentalConditionSerializer, 400: "Ошибка"},
    )

    rental_detail = extend_schema(
        methods=["GET"],
        summary="🔍 Детали условий аренды",
        description="Получает условия аренды по ID.",
        responses={200: RentalConditionSerializer, 404: "Не найдено"},
    )

    rental_update = extend_schema(
        methods=["PUT", "PATCH"],
        summary="✏️ Обновить условия аренды",
        description="Обновляет условия аренды. Можно использовать `PUT` или `PATCH`.",
        request=RentalConditionSerializer,
        responses={200: RentalConditionSerializer, 400: "Ошибка", 404: "Не найдено"},
    )


class RentalDiscountSwagger:
    """Документация для API тарифных планов (скидок на аренду)."""

    discount_list = extend_schema(
        methods=["GET"],
        summary="📜 Список тарифных планов",
        description="Возвращает список всех тарифных планов (скидок).",
        responses={200: RentalDiscountSerializer(many=True)},
    )

    discount_create = extend_schema(
        methods=["POST"],
        summary="📝 Добавить тарифный план",
        description="Создаёт новый тарифный план (скидку).",
        request=RentalDiscountSerializer,
        responses={201: RentalDiscountSerializer, 400: "Ошибка"},
    )

    discount_detail = extend_schema(
        methods=["GET"],
        summary="🔍 Детали тарифного плана",
        description="Получает тарифный план по ID.",
        responses={200: RentalDiscountSerializer, 404: "Не найдено"},
    )

    discount_update = extend_schema(
        methods=["PUT", "PATCH"],
        summary="✏️ Обновить тарифный план",
        description="Обновляет тарифный план. Можно использовать `PUT` или `PATCH`.",
        request=RentalDiscountSerializer,
        responses={200: RentalDiscountSerializer, 400: "Ошибка", 404: "Не найдено"},
    )


class RentalSwagger:
    """Документация для API аренды."""

    rental_create = extend_schema(
        methods=["POST"],
        summary="Создание аренды и возвращает общую стоимость аренды.",
        description="Создаёт новую аренду и возвращает общую стоимость аренды.",
        request=RentalSerializer(),
        responses={201: RentalSerializer(), 400: "Ошибка"},
    )


from drf_spectacular.utils import extend_schema


class CarOptionSwagger:
    list = extend_schema(
        methods=["GET"],
        summary="Список опций автомобилей",
        description="Получить список всех дополнительных опций автомобилей",
        responses={200: CarOptionSerializer(many=True)},
    )
    create = extend_schema(
        methods=["POST"],
        summary="Создание опции автомобиля",
        description="Создать новую дополнительную опцию",
        request=CarOptionSerializer,
        responses={201: CarOptionSerializer},
    )
    retrieve = extend_schema(
        methods=["GET"],
        summary="Получение информации об опции автомобиля",
        description="Получить информацию о конкретной дополнительной опции",
        responses={200: CarOptionSerializer},
    )
    update = extend_schema(
        methods=["PUT"],
        summary="Обновление опции автомобиля",
        description="Обновить информацию о дополнительной опции",
        request=CarOptionSerializer,
        responses={200: CarOptionSerializer},
    )
    partial_update = extend_schema(
        methods=["PATCH"],
        summary="Частичное обновление опции автомобиля",
        description="Частичное обновление информации о дополнительной опции",
        request=CarOptionSerializer,
        responses={200: CarOptionSerializer},
    )
    destroy = extend_schema(
        methods=["DELETE"],
        summary="Удаление опции автомобиля",
        description="Удалить дополнительную опцию",
        responses={204: "No Content"},
    )


class CarEquipmentSwagger:
    list = extend_schema(
        methods=["GET"],
        summary="Список комплектаций автомобилей",
        description="Получить список всех комплектаций автомобилей",
        responses={200: CarEquipmentSerializer(many=True)},
    )
    create = extend_schema(
        methods=["POST"],
        summary="Создание комплектации автомобиля",
        description="Создать новую комплектацию автомобиля",
        request=CarEquipmentSerializer,
        responses={201: CarEquipmentSerializer},
    )
    retrieve = extend_schema(
        methods=["GET"],
        summary="Получение информации о комплектации автомобиля",
        description="Получить информацию о конкретной комплектации автомобиля",
        responses={200: CarEquipmentSerializer},
    )
    update = extend_schema(
        methods=["PUT"],
        summary="Обновление комплектации автомобиля",
        description="Обновить информацию о комплектации автомобиля",
        request=CarEquipmentSerializer,
        responses={200: CarEquipmentSerializer},
    )
    partial_update = extend_schema(
        methods=["PATCH"],
        summary="Частичное обновление комплектации автомобиля",
        description="Частичное обновление информации о комплектации автомобиля",
        request=CarEquipmentSerializer,
        responses={200: CarEquipmentSerializer},
    )
    destroy = extend_schema(
        methods=["DELETE"],
        summary="Удаление комплектации автомобиля",
        description="Удалить комплектацию автомобиля",
        responses={204: "No Content"},
    )
