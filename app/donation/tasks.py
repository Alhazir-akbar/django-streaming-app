from celery import shared_task
from .models import Donation

@shared_task
def process_donation(donation_id):
    donation = Donation.objects.get(id=donation_id)
    # Logika untuk memproses donasi, misalnya menghubungi payment gateway
    # Misalnya, jika sukses:
    donation.payment_status = 'completed'
    donation.save()
    # Kirim notifikasi atau lakukan tindakan lain
