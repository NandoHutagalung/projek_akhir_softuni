from django.contrib import admin
from .models import Pesanan, DetailPesanan

class DetailPesananInline(admin.TabularInline):
    model = DetailPesanan
    extra = 1

class PesananAdmin(admin.ModelAdmin):
    list_display = ('user', 'meja', 'tanggal_pemesanan', 'durasi_meja', 'get_total_harga', 'status', 'waktu_selesai', 'waktu_notif', 'is_send', 'notifikasi_dikirim')
    inlines = [DetailPesananInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.hitung_total_harga()

    def delete_model(self, request, obj):
        obj.hitung_total_harga()
        super().delete_model(request, obj)

    def get_total_harga(self, obj):
        return f"Rp {obj.total_harga:,.0f}"
    get_total_harga.short_description = 'Total Harga'

admin.site.register(Pesanan, PesananAdmin)
admin.site.register(DetailPesanan)
