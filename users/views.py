from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from hotels.models import Hotel
from hotels.serializers import HotelSerializer
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer
from tours.models import Guide, TourOperator
from tours.serializers import GuideSerializer, TourOperatorSerializer
from .models import CustomUser, SMSVerification
from .serializers import CustomUserSerializer, SMSVerificationSerializer
from .service import send_verification_sms




class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class OwnerObjectsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

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
# views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с уведомлениями пользователей.
    """
    permission_classes = [IsAuthenticated]   # Доступ только для авторизованных пользователей
    serializer_class = NotificationSerializer

    def get_queryset(self):
        """
        Получаем только уведомления для текущего пользователя.
        """
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """
        Создаем уведомление для текущего пользователя и отправляем email.
        """
        # Получаем данные для создания уведомления (можно передать их через сериализатор)
        user = self.request.data.get('user')  # Получатель уведомления (например, из данных запроса)
        
        # Проверяем, что указанный получатель существует
        if not user:
            return Response({'detail': 'Получатель не указан.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Получаем пользователя по ID (или другим параметрам)
            user = CustomUser.objects.get(id=user)
            print(user, self.request.user)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Указываем отправителя как текущего пользователя
        notification = serializer.save(user=user, sender=self.request.user)

    #
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    

    def partial_update(self, request, *args, **kwargs):
        """
        Обновление уведомления (например, пометить как прочитанное).
        Позволяет только получателю уведомления пометить его как прочитанное.
        """
        instance = self.get_object()
        
        # Проверяем, что текущий пользователь является получателем уведомления
        if request.user != instance.user:
            return Response(
                {'detail': 'У вас нет прав на обновление этого уведомления.'},
                status=status.HTTP_403_FORBIDDEN
            )
        print(instance.user)
        # Помечаем уведомление как прочитанное
        instance.is_read = True
        instance.save()
        return Response(
            {'detail': 'Уведомление помечено как прочитанное.'},
            status=status.HTTP_200_OK
    )
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Booking
from .serializers import BookingSerializer
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

class BookingViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing bookings.
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access the endpoint

    def get_queryset(self):
        """
        This view returns a list of all the bookings for the currently authenticated user.
        """
        user = self.request.user
        return Booking.objects.filter(user=user)  # Filter bookings for the current authenticated user

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific booking by model_name (e.g., 'tour', 'hotel') and object_id.
        """
        model_name = kwargs.get('model_name')
        object_id = kwargs.get('object_id')

        try:
            # Get the ContentType object based on the model_name
            content_type = ContentType.objects.get(model=model_name)

            # Fetch the booking related to the model and ID
            booking = Booking.objects.get(content_type=content_type, object_id=object_id, user=request.user)
            
            # Serialize and return the booking
            serializer = self.get_serializer(booking)
            return Response(serializer.data)
        
        except ContentType.DoesNotExist:
            raise NotFound(f"Content type with the model name '{model_name}' not found.")
        except Booking.DoesNotExist:
            raise NotFound(f"Booking for {model_name} with ID {object_id} not found for this user.")

    def perform_create(self, serializer):
        # Ensure that the user is authenticated and set the user field
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Overridden to ensure the booking belongs to the authenticated user.
        """
        # Retrieve the booking instance being updated
        instance = self.get_object()

        # Ensure that the authenticated user is the owner of the booking
        if instance.user != self.request.user:
            raise NotFound("You can only update your own bookings.")

        # Proceed with saving the updated booking
        serializer.save()
    def destroy(self, request, *args, **kwargs):
        """
        Delete a booking for the authenticated user.
        """
        # Ensure the booking belongs to the current user
        instance = self.get_object()
        if instance.user != request.user:
            raise NotFound("You can only delete your own bookings.")
        
        # Call the default destroy method to handle the deletion
        return super().destroy(request, *args, **kwargs)
