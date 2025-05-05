from drf_spectacular.utils import extend_schema
from .serializers import NotificationSettingsSerializer


class NotificationSettingsSwagger:
    """Документация для API настроек уведомлений."""

    settings_list = extend_schema(
        methods=["GET"],
        summary="📋 Получить настройки уведомлений",
        description="Возвращает текущие настройки уведомлений пользователя.",
        responses={200: NotificationSettingsSerializer(many=False)},
    )

    settings_create = extend_schema(
        methods=["POST"],
        summary="Создать настройки уведомлений",
        description="Создаёт новые настройки уведомлений для текущего пользователя.",
        request=NotificationSettingsSerializer,
        responses={
            201: NotificationSettingsSerializer,
            400: "Ошибка валидации",
            403: "Доступ запрещён (уже есть настройки)",
        },
    )

    settings_detail = extend_schema(
        methods=["GET"],
        summary="🔍 Получить настройки по ID",
        description="Получает настройки уведомлений по ID (только свои настройки).",
        responses={200: NotificationSettingsSerializer, 404: "Настройки не найдены"},
    )

    settings_update = extend_schema(
        methods=["PUT"],
        summary="✏️ Обновить настройки",
        description="Полное обновление настроек уведомлений.",
        request=NotificationSettingsSerializer,
        responses={
            200: NotificationSettingsSerializer,
            400: "Ошибка валидации",
            404: "Настройки не найдены",
        },
    )

    settings_partial_update = extend_schema(
        methods=["PATCH"],
        summary="✏️ Частично обновить настройки",
        description="Частичное обновление настроек уведомлений.",
        request=NotificationSettingsSerializer,
        responses={
            200: NotificationSettingsSerializer,
            400: "Ошибка валидации",
            404: "Настройки не найдены",
        },
    )

    settings_delete = extend_schema(
        methods=["DELETE"],
        summary="🗑️ Удалить настройки",
        description="Удаляет настройки уведомлений пользователя.",
        responses={204: "Настройки удалены", 404: "Настройки не найдены"},
    )
