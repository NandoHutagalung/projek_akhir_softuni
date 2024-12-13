from django.core.management.base import BaseCommand
from django.utils import timezone
from pesanan.models import Pesanan
from meja_biliar.models import MejaBiliar

class Command(BaseCommand):
    help = 'Memperbarui status pesanan yang sudah dibuat lebih dari durasi_meja dan memperbarui status MejaBiliar'

    def handle(self, *args, **kwargs):
        # Hitung waktu sekarang
        sekarang = timezone.now()

        # Query untuk memperbarui status pesanan yang sudah melewati durasi_meja
        pesanan = Pesanan.objects.all()
        updated_count = 0

        for p in pesanan:
            # Periksa apakah tanggal_pemesanan + durasi_meja sudah melebihi waktu sekarang
            if p.tanggal_pemesanan + timezone.timedelta(hours=p.durasi_meja) <= sekarang:
                if p.status == 'aktif':  # Hanya ubah status jika masih 'aktif'
                    # Ubah status pesanan menjadi 'tidak aktif'
                    p.status = 'tidak aktif'
                    p.save()

                    # Perbarui status MejaBiliar jika status pesanan diubah
                    if p.meja.status == 'full':
                        p.meja.status = 'ada'
                        p.meja.save(update_fields=['status'])

                    updated_count += 1

        self.stdout.write(f'{updated_count} pesanan diperbarui dan status meja diperbarui.')
