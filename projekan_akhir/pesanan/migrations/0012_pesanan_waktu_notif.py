# Generated by Django 5.1.3 on 2024-12-06 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesanan', '0011_pesanan_waktu_selesai_alter_pesanan_is_send'),
    ]

    operations = [
        migrations.AddField(
            model_name='pesanan',
            name='waktu_notif',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]