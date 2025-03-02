from rest_framework import serializers
from .models import Entertainment


class EntertainmentSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Entertainment
        fields = "__all__"

    def get_rating(self, obj):
        return obj.calculate_rating()
