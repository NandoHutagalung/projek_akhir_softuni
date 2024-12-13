from django.contrib import admin
from .models import MejaBiliar

@admin.register(MejaBiliar)
class MejaBiliarAdmin(admin.ModelAdmin):
    list_display = ('no_meja', 'harga_siang', 'harga_malam', 'status')  

