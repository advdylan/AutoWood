# Generated by Django 5.0.4 on 2024-04-22 17:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_remove_element_count_productelement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='wood_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.wood'),
        ),
        migrations.DeleteModel(
            name='WoodType',
        ),
    ]