# Generated by Django 5.0.4 on 2024-04-22 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_accessorytype_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]