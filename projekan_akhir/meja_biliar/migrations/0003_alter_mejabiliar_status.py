# Generated by Django 5.1.3 on 2024-12-04 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meja_biliar', '0002_alter_mejabiliar_options_mejabiliar_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mejabiliar',
            name='status',
            field=models.CharField(choices=[('full', 'Full'), ('ada', 'Ada'), ('perbaikan', 'Perbaikan')], default='ada', max_length=20),
        ),
    ]
