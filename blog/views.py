from Kavkaztome.permissions import IsOwnerOnly
from rest_framework import viewsets
from .models import Blog
from .serializers import BlogSerializer


class BlogViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с блоками новостей.
    Позволяет работать как с одним обьектом,
    так и с набором обьектов при get запросе."""

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (IsOwnerOnly,)

    def get_object(self):
        """Метод получения обьекта по слагу."""
        slug = self.kwargs["slug"]
        return self.get_queryset().get(url=slug)
