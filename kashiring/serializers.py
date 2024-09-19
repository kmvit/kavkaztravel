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
        fields = ("year",)


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
    Сериализатор для создания и изменения обьектов модели.
    """
    brand =serializers.PrimaryKeyRelatedField(read_only=True)
    model = serializers.PrimaryKeyRelatedField(read_only=True)
    year =  serializers.PrimaryKeyRelatedField(read_only=True)
    color =  serializers.PrimaryKeyRelatedField(read_only=True)
    body_type = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Auto
        fields = '__all__'


class AutoGETSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField(read_only=True)
    model = serializers.StringRelatedField(read_only=True)
    year =  YearSerializer()
    color =  serializers.StringRelatedField(read_only=True)
    body_type = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Auto
        fields = ("id", "brand", "model", "year", "color", "body_type")


class AutoMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auto
        fields = ('name',)


class CompanyAutoSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Company.
    """
    auto = AutoMiniSerializer(many=True)

    class Meta:
        model = Company
        fields = ("name", "auto",)

class CompanySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Company.
    """
    
    class Meta:
        model = Company
        fields = ("name",)
