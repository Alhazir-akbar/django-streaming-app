# app/donation/views.py

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Donation
from .serializers import DonationSerializer

class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        donation = serializer.save(user=self.request.user)
        # Kirim notifikasi setelah donasi berhasil dibuat
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'stream_{donation.stream.id}',
            {
                'type': 'stream_message',
                'message': f'New donation from {donation.user.username}: ${donation.amount}'
            }
        )

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        donation = self.get_object()
        if donation.payment_method == 'manual':
            donation.payment_status = 'completed'
            donation.save()
            return Response({'status': 'donation confirmed'})
        return Response({'status': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        stream_id = self.request.query_params.get('stream')
        if stream_id:
            return self.queryset.filter(stream_id=stream_id)
        return self.queryset
