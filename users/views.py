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
from .sms_service import send_verification_sms


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
