from rest_framework import viewsets
from .models import Blog
from .serializers import BlogSerializer

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_object(self):
        slug = self.kwargs['slug']
        return self.get_queryset().get(slug=slug)