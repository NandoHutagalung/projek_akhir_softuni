from django.db import models

class MejaBiliar(models.Model):
    STATUS_CHOICES = [
        ('full', 'Full'),
        ('ada', 'Ada'),
        ('perbaikan', 'Perbaikan'),
    ]

    no_meja = models.CharField(max_length=20)
    harga_siang = models.DecimalField(max_digits=10, decimal_places=2)
    harga_malam = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ada')  

    def __str__(self):
        return f"Meja {self.no_meja} ({self.status})"

