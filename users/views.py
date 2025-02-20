import logging

from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.apps import apps
from django.conf import settings

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework.views import APIView

from hotels.models import Hotel
from hotels.serializers import HotelSerializer
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer
from tours.models import Guide, TourOperator
from tours.serializers import GuideSerializer, TourOperatorSerializer
from .models import CustomUser, SMSVerification, Notification, Booking, UserNotificationChannel
from .serializers import CustomUserSerializer, SMSVerificationSerializer, NotificationSerializer, BookingSerializer
from .service import send_notification, send_verification_sms

logger = logging.getLogger(__name__)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class OwnerObjectsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get", "post", "put", "delete"])
    def hotels(self, request):
        if request.method == "GET":
            hotels = Hotel.objects.filter(owner=request.user)
            serializer = HotelSerializer(hotels, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            serializer = HotelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        elif request.method == "PUT":
            hotel = Hotel.objects.get(id=request.data["id"], owner=request.user)
            serializer = HotelSerializer(hotel, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        elif request.method == "DELETE":
            hotel = Hotel.objects.get(id=request.data["id"], owner=request.user)
            hotel.delete()
            return Response(status=204)

    @action(detail=False, methods=["get", "post", "put", "delete"])
    def restaurants(self, request):
        if request.method == "GET":
            restaurants = Restaurant.objects.filter(owner=request.user)
            serializer = RestaurantSerializer(restaurants, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            serializer = RestaurantSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        elif request.method == "PUT":
            restaurant = Restaurant.objects.get(
                id=request.data["id"], owner=request.user
            )
            serializer = RestaurantSerializer(
                restaurant, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        elif request.method == "DELETE":
            restaurant = Restaurant.objects.get(
                id=request.data["id"], owner=request.user
            )
            restaurant.delete()
            return Response(status=204)

    @action(detail=False, methods=["get", "post", "put", "delete"])
    def guides(self, request):
        if request.method == "GET":
            guides = Guide.objects.filter(owner=request.user)
            serializer = GuideSerializer(guides, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            serializer = GuideSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        elif request.method == "PUT":
            guide = Guide.objects.get(id=request.data["id"], owner=request.user)
            serializer = GuideSerializer(guide, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        elif request.method == "DELETE":
            guide = Guide.objects.get(id=request.data["id"], owner=request.user)
            guide.delete()
            return Response(status=204)

    @action(detail=False, methods=["get", "post", "put", "delete"])
    def touroperators(self, request):
        if request.method == "GET":
            touroperators = TourOperator.objects.filter(owner=request.user)
            serializer = TourOperatorSerializer(touroperators, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            serializer = TourOperatorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        elif request.method == "PUT":
            touroperator = TourOperator.objects.get(
                id=request.data["id"], owner=request.user
            )
            serializer = TourOperatorSerializer(
                touroperator, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        elif request.method == "DELETE":
            touroperator = TourOperator.objects.get(
                id=request.data["id"], owner=request.user
            )
            touroperator.delete()
            return Response(status=204)


class SendVerificationCodeAPIView(APIView):
    """Отправка кода подтверждения на указанный номер."""

    def post(self, request):
        phone_number = request.data.get("phone_number")

        if not phone_number:
            return Response(
                {"error": "Phone number is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Отправка SMS с кодом
        verification = send_verification_sms(phone_number)
        serializer = SMSVerificationSerializer(verification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyCodeAPIView(APIView):
    """Проверка введенного пользователем кода."""

    def post(self, request):
        phone_number = request.data.get("phone_number")
        entered_code = request.data.get("verification_code")

        if not phone_number or not entered_code:
            return Response(
                {"error": "Phone number and verification code are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Получаем запись для указанного номера телефона
        try:
            verification = SMSVerification.objects.get(phone_number=phone_number)
        except SMSVerification.DoesNotExist:
            return Response(
                {"error": "Verification record not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Проверка на истечение срока действия кода
        if verification.is_expired():
            return Response(
                {"error": "Verification code has expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Проверка введенного кода
        if entered_code == verification.verification_code:
            return Response(
                {"message": "Code verified successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid verification code"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class BookingViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для управления бронированиями.
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]  # Обеспечиваем доступ только для аутентифицированных пользователей

    def get_queryset(self):
        """
        Этот метод возвращает список всех бронирований для текущего аутентифицированного пользователя.
        """
        user = self.request.user
        return Booking.objects.filter(user=user)  # Фильтруем бронирования по текущему аутентифицированному пользователю

    def retrieve(self, request, *args, **kwargs):
        """
        Получить конкретное бронирование по имени модели (например, 'tour', 'hotel') и объекту (ID).
        """
        model_name = kwargs.get('model_name')
        object_id = kwargs.get('object_id')

        try:
            # Получаем объект ContentType по имени модели
            content_type = ContentType.objects.get(model=model_name)

            # Извлекаем бронирование, связанное с моделью и ID
            booking = Booking.objects.get(content_type=content_type, object_id=object_id, user=request.user)
            
            # Сериализуем и возвращаем данные бронирования
            serializer = self.get_serializer(booking)
            return Response(serializer.data)
        
        except ContentType.DoesNotExist:
            raise NotFound(f"Тип контента с именем модели '{model_name}' не найден.")
        except Booking.DoesNotExist:
            raise NotFound(f"Бронирование для {model_name} с ID {object_id} не найдено для этого пользователя.")

    def perform_create(self, serializer):
        """
        Создание нового бронирования.
        Обеспечиваем, что в поле user будет установлен текущий аутентифицированный пользователь.
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Переопределенный метод для обеспечения того, чтобы бронирование принадлежало аутентифицированному пользователю.
        """
        # Извлекаем экземпляр бронирования, который мы обновляем
        instance = self.get_object()

        # Проверяем, что бронирование принадлежит текущему пользователю
        if instance.user != self.request.user:
            raise NotFound("Вы можете обновить только свои собственные бронирования.")

        # Продолжаем сохранение обновленного бронирования
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        Удаление бронирования для аутентифицированного пользователя.
        """
        # Проверяем, что бронирование принадлежит текущему пользователю
        instance = self.get_object()
        if instance.user != request.user:
            raise NotFound("Вы можете удалить только свои собственные бронирования.")
        
        # Вызываем стандартный метод destroy для обработки удаления
        return super().destroy(request, *args, **kwargs)



class NotificationViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для создания, получения и обновления уведомлений.
    Отправка уведомлений через каналы связи: email или REST API.
    """
    queryset = Notification.objects.all()  # Получаем все уведомления
    serializer_class = NotificationSerializer  # Сериализатор для уведомлений

    def get_queryset(self):
        """
        Возвращаем уведомления только для текущего пользователя (если пользователь авторизован).
        """
        user = self.request.user
        if user.is_authenticated:
            return Notification.objects.filter(user=user)
        return Notification.objects.none()  # Если пользователь не аутентифицирован, не показываем уведомления

    def perform_create(self, serializer):
        """
        Создаем уведомление для пользователя и отправляем его через выбранные каналы связи.
        """
        user_id = self.request.data.get('user')  # Получатель уведомления
        if not user_id:
            return Response({'detail': 'Получатель не указан.'}, status=status.HTTP_400_BAD_REQUEST)

        # Получаем модель пользователя с помощью get_object_or_404 для получения пользователя
        UserModel = apps.get_model(settings.AUTH_USER_MODEL)
        user = get_object_or_404(UserModel, id=user_id)

        # Создаем уведомление
        notification = serializer.save(user=user, sender=self.request.user)

        # Получаем настройки канала уведомлений для пользователя
        notification_channel = get_object_or_404(UserNotificationChannel, user=user)

        # Отправляем уведомление через активированный канал
        if send_notification(notification, notification_channel.channel_type):
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'detail': 'Не удалось отправить уведомление.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        """
        Обновление уведомления. Помечаем уведомление как прочитанное.
        Проверяется, что уведомление принадлежит текущему пользователю.
        """
        try:
            # Получаем уведомление по первичному ключу (pk) из kwargs
            notification = Notification.objects.get(pk=kwargs['pk'])

            # Проверяем, что уведомление принадлежит текущему пользователю
            if notification.user != request.user:
                return Response({"detail": "Уведомление не предназначено для этого пользователя."},
                                status=status.HTTP_403_FORBIDDEN)

            # Помечаем уведомление как прочитанное
            notification.is_read = True
            notification.save()

            # Возвращаем успешное сообщение
            return Response({"message": "Сообщение помечено как прочитанное."}, status=status.HTTP_200_OK)

        except Notification.DoesNotExist:
            # Возвращаем ошибку, если уведомление не найдено
            return Response({"detail": "Уведомление не найдено."}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import UserNotificationChannel
from .serializers import UserNotificationChannelSerializer

class UserNotificationChannelViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для управления каналами уведомлений пользователей.
    Обеспечивает CRUD операции для модели UserNotificationChannel.
    """
    queryset = UserNotificationChannel.objects.all()
    serializer_class = UserNotificationChannelSerializer
    permission_classes = [IsAuthenticated]  # Обеспечиваем доступ только для аутентифицированных пользователей

    def get_queryset(self):
        """
        Возвращает список каналов уведомлений для текущего аутентифицированного пользователя.
        Каждый пользователь может иметь только один канал уведомлений.
        """
        return UserNotificationChannel.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Создание нового канала уведомлений для пользователя.
        """
        # Обеспечиваем, что канал уведомлений будет принадлежать текущему аутентифицированному пользователю
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        """
        Обновление канала уведомлений.
        Обеспечиваем, что обновляемый канал принадлежит текущему пользователю.
        """
        instance = self.get_object()
        if instance.user != self.request.user:
            raise NotFound("Вы можете обновить только свой собственный канал уведомлений.")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        Удаление канала уведомлений для аутентифицированного пользователя.
        """
        instance = self.get_object()
        if instance.user != request.user:
            raise NotFound("Вы можете удалить только свой собственный канал уведомлений.")
        return super().destroy(request, *args, **kwargs)
