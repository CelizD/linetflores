# Generated by Django 5.2.4 on 2025-07-10 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0005_color_material_variedad'),
    ]

    operations = [
        migrations.AddField(
            model_name='flor',
            name='categoria',
            field=models.CharField(choices=[('rosas', 'Rosas'), ('tulipanes', 'Tulipanes'), ('girasoles', 'Girasoles'), ('mix', 'Mix de flores'), ('especial', 'Edición Especial'), ('otros', 'Otros')], default='otros', max_length=50),
        ),
        migrations.AddField(
            model_name='flor',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='flor',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
