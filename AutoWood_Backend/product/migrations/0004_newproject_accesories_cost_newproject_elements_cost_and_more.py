# Generated by Django 5.0 on 2024-08-31 07:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_rename_percent_additionak_margin_newproject_percent_additional_margin'),
    ]

    operations = [
        migrations.AddField(
            model_name='newproject',
            name='accesories_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='newproject',
            name='elements_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='projectworktime',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_worktime', to='product.newproject'),
        ),
    ]