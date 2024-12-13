from django.db import models

class Menu(models.Model):
    nama_menu = models.CharField(max_length=255)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.ImageField(upload_to='menu_photos/')

    def __str__(self):
        return self.nama_menu
