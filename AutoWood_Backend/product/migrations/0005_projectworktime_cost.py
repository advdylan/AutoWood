# Generated by Django 5.0 on 2024-09-03 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_newproject_accesories_cost_newproject_elements_cost_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectworktime',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=2, max_digits=10),
            preserve_default=False,
        ),
    ]