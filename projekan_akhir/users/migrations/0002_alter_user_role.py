# Generated by Django 5.1.3 on 2024-12-05 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('staff', 'Staff'), ('member', 'Member')], default='viewer', max_length=20),
        ),
    ]
