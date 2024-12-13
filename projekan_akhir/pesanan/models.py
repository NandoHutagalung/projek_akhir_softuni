from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from menu.models import Menu
from meja_biliar.models import MejaBiliar
from users.models import User
from django.utils.timezone import now, localtime
from datetime import timedelta

class Pesanan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meja = models.ForeignKey(MejaBiliar, on_delete=models.CASCADE)
    tanggal_pemesanan = models.DateTimeField(auto_now_add=True)
    durasi_meja = models.PositiveIntegerField(help_text="Durasi pemesanan dalam jam", default=1)
    total_harga = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=20, default='aktif')
    is_send = models.BooleanField(default=False)
    waktu_selesai = models.DateTimeField(editable=False, null=True, blank=True)
    waktu_notif = models.DateTimeField(editable=False, null=True, blank=True)
    notifikasi_dikirim = models.BooleanField(default=False)

    def clean(self):
        self.meja.refresh_from_db()
        if not self.id and self.meja.status != 'ada':
            raise ValidationError(f"Meja {self.meja.no_meja} tidak dapat dipesan karena statusnya adalah '{self.meja.get_status_display()}'.")
        super().clean()

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.clean() 
            super().save(*args, **kwargs)

            if self.meja.status == 'ada':
                self.meja.status = 'full'
                self.meja.save(update_fields=['status'])

    def hitung_total_harga(self):
        total_menu = sum(
            detail.menu.harga * detail.jumlah for detail in self.detail_pesanan.all()
        )

        current_hour = timezone.now().hour
        if 8 <= current_hour < 16: 
            harga_per_jam = Decimal(self.meja.harga_siang)
        else: 
            harga_per_jam = Decimal(self.meja.harga_malam)
        
        if self.durasi_meja >= 3:
            harga_per_jam = harga_per_jam * Decimal("0.9")
        else:
            harga_per_jam = harga_per_jam * 1

        if self.durasi_meja >= 3:
            total_menu = total_menu * Decimal("0.7")
        else:
            total_menu = total_menu * 1

        total_meja = self.durasi_meja * harga_per_jam
        self.total_harga = total_menu + total_meja
        self.waktu_selesai = self.tanggal_pemesanan + timedelta(hours=self.durasi_meja)
        self.waktu_notif = self.waktu_selesai - timedelta(seconds=3450)
        self.save(update_fields=["total_harga", "waktu_selesai", "waktu_notif"])

    def batal_pesanan(self):
        with transaction.atomic():
            if self.meja.status == 'full':
                self.meja.status = 'ada'
                self.meja.save(update_fields=['status'])
            self.delete()


    def __str__(self):
        return f"Pesanan oleh {self.user.username} di Meja {self.meja.no_meja} pada {self.tanggal_pemesanan}"


class DetailPesanan(models.Model):
    pesanan = models.ForeignKey(
        Pesanan, on_delete=models.CASCADE, related_name="detail_pesanan"
    )
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.pesanan.hitung_total_harga()

    def __str__(self):
        return f"{self.jumlah} x {self.menu.nama_menu} untuk Pesanan {self.pesanan.id}"
