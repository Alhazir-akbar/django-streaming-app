# app/comment/views.py

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Comment
from .serializers import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        comment = serializer.save(user=self.request.user)
        # Kirim notifikasi setelah komentar berhasil dibuat
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'stream_{comment.stream.id}',
            {
                'type': 'stream_message',
                'message': f'New comment from {comment.user.username}: {comment.content}'
            }
        )

    def get_queryset(self):
        stream_id = self.kwargs.get('stream_id')
        if stream_id:
            return self.queryset.filter(stream__id=stream_id)
        return self.queryset
