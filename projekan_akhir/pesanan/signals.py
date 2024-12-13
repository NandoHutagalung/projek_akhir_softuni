from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pesanan, DetailPesanan
from django.utils import timezone
from decimal import Decimal

@receiver(post_save, sender=DetailPesanan)
def update_total_harga(sender, instance, **kwargs):
    pesanan = instance.pesanan
    pesanan.hitung_total_harga()
