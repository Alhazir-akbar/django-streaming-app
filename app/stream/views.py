# app/stream/views.py

from rest_framework import viewsets
from .models import Stream
from .serializers import StreamSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class StreamViewSet(viewsets.ModelViewSet):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
