# Generated by Django 5.0 on 2024-09-03 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_projectworktime_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectworktime',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=10),
        ),
    ]