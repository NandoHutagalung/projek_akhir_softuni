from django.contrib import admin
from .models import Menu

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('nama_menu', 'harga', 'foto')
    search_fields = ('nama_menu',)
    list_filter = ('harga',)
    ordering = ('nama_menu',)


