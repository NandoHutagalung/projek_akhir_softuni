# Generated by Django 5.1.3 on 2024-12-05 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesanan', '0010_pesanan_is_send'),
    ]

    operations = [
        migrations.AddField(
            model_name='pesanan',
            name='waktu_selesai',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='pesanan',
            name='is_send',
            field=models.BooleanField(default=False),
        ),
    ]