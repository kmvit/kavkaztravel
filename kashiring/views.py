from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import (
    Brand, Model, Year, Color, BodyType, Auto, Foto, Company
)
from .serializers import (
    BrandSerializer, ModelSerializer, YearSerializer, ColorSerializer,
    BodyTypeSerializer, AutoSerializer, FotoSerializer, CompanySerializer
)


class BrandViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on Brand models.
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on Model models.
    """
    queryset = Model.objects.all()
    serializer_class = ModelSerializer


class YearViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on Year models.
    """
    queryset = Year.objects.all()
    serializer_class = YearSerializer


class ColorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on Color models.
    """
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class BodyTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on BodyType models.
    """
    queryset = BodyType.objects.all()
    serializer_class = BodyTypeSerializer


class AutoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on Auto models.
    """
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer

    def get_related_objects(self, data):
        """
        Helper method to get related objects from the request data.
        """
        try:
            brand = Brand.objects.get(id=int(data.get("brand")))
            model = Model.objects.get(id=int(data.get('model')))
            year = Year.objects.get(id=int(data.get('year')))
            color = Color.objects.get(id=int(data.get('color')))
            body_type = BodyType.objects.get(id=int(data.get('body_type')))
        except (Brand.DoesNotExist, Model.DoesNotExist, Year.DoesNotExist,
                Color.DoesNotExist, BodyType.DoesNotExist) as e:
            raise serializers.ValidationError({"detail": str(e)})

        return brand, model, year, color, body_type

    def perform_create(self, serializer):
        brand, model, year, color, body_type = self.get_related_objects(
            self.request.data
        )
        serializer.save(
            brand=brand,
            model=model,
            color=color,
            year=year,
            body_type=body_type
        )

    def perform_update(self, serializer):
        data = self.request.data
        brand, model, year, color, body_type = self.get_related_objects({
            'brand': data.get("brand", self.get_object().brand.id),
            'model': data.get('model', self.get_object().model.id),
            'year': data.get('year', self.get_object().year.id),
            'color': data.get('color', self.get_object().color.id),
            'body_type': data.get('body_type', self.get_object().body_type.id)
        })
        serializer.save(
            brand=brand,
            model=model,
            color=color,
            year=year,
            body_type=body_type
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FotoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on Foto models.
    """
    queryset = Foto.objects.all()
    serializer_class = FotoSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on Company models.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
