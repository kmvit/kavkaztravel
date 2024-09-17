from rest_framework import serializers
from .models import (
    Brand, Model, Year, Color, BodyType, Auto, Foto, Company
)

class BrandSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Brand.
    """
    class Meta:
        model = Brand
        fields = '__all__'


class ModelSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Model.
    """
    class Meta:
        model = Model
        fields = '__all__'


class YearSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Year.
    """
    class Meta:
        model = Year
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Color.
    """
    class Meta:
        model = Color
        fields = '__all__'


class BodyTypeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели BodyType.
    """
    class Meta:
        model = BodyType
        fields = '__all__'


class AutoSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Auto.
    """
    brand = serializers.StringRelatedField(read_only=True)
    model = serializers.StringRelatedField(read_only=True)
    year =  serializers.StringRelatedField(read_only=True)
    color =  serializers.StringRelatedField(read_only=True)
    body_type = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Auto
        fields = '__all__'


class FotoSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Foto.
    """
    auto = AutoSerializer()

    class Meta:
        model = Foto
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Company.
    """
    auto = AutoSerializer(many=True)

    class Meta:
        model = Company
        fields = '__all__'
