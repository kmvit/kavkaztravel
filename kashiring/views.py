from rest_framework import viewsets
from .models import (
    Brand, Model, Year, Color, BodyType, Auto, Foto, Company
)
from .serializers import (
    BrandSerializer, ModelSerializer, YearSerializer, ColorSerializer,
    BodyTypeSerializer, AutoSerializer, FotoSerializer, CompanySerializer
)
from django.shortcuts import get_object_or_404 


class BrandViewSet(viewsets.ModelViewSet):
    """
    Представление для CRUD операций с моделями Brand.
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ModelViewSet(viewsets.ModelViewSet):
    """
    Представление для CRUD операций с моделями Model.
    """
    queryset = Model.objects.all()
    serializer_class = ModelSerializer


class YearViewSet(viewsets.ModelViewSet):
    """
    Представление для CRUD операций с моделями Year.
    """
    queryset = Year.objects.all()
    serializer_class = YearSerializer


class ColorViewSet(viewsets.ModelViewSet):
    """
    Представление для CRUD операций с моделями Color.
    """
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class BodyTypeViewSet(viewsets.ModelViewSet):
    """
    Представление для CRUD операций с моделями BodyType.
    """
    queryset = BodyType.objects.all()
    serializer_class = BodyTypeSerializer


class AutoViewSet(viewsets.ModelViewSet):
    """
    Представление для CRUD операций с моделями Auto.
    """
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer

    def perform_create(self, serializer): 
        brand_id = self.kwargs.get('brand_id') 
        brand = get_object_or_404(Brand, id=brand_id) 
        model_id = self.kwargs.get('model_id') 
        model = get_object_or_404(Model, id=model_id) 
        year_id = self.kwargs.get('year_id') 
        year = get_object_or_404(Year, id=year_id) 
        color_id = self.kwargs.get('сolor_id') 
        color = get_object_or_404(Year, id=color_id) 
        body_type_id = self.kwargs.get('body_type_id') 
        body_type = get_object_or_404(Year, id=body_type_id) 


        serializer.save(brand=brand, model=model, year=year, color=color, body_type=body_type) 


class FotoViewSet(viewsets.ModelViewSet):
    """
    Представление для CRUD операций с моделями Foto.
    """
    queryset = Foto.objects.all()
    serializer_class = FotoSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    Представление для CRUD операций с моделями Company.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
