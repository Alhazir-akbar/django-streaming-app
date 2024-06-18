# app/donation/views.py

from rest_framework import viewsets
from .models import Donation
from .serializers import DonationSerializer
from rest_framework.permissions import IsAuthenticated
from .tasks import process_donation

class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        donation = serializer.save()
        # Panggil tugas Celery untuk memproses donasi
        process_donation.delay(donation.id)
