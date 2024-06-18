# app/stream/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Stream
from .serializers import StreamSerializer

class StreamViewSet(viewsets.ModelViewSet):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        stream = self.get_object()
        stream.status = 'active'
        stream.save()
        return Response({'status': 'stream started'})

    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        stream = self.get_object()
        stream.status = 'inactive'
        stream.save()
        return Response({'status': 'stream stopped'})
