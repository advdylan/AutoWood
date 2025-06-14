# Generated by Django 5.0 on 2025-06-15 10:39

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_rename_accesories_cost_newproject_accessories_cost_and_more'),
        ('production', '0002_alter_productionstage_shortcut'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='production',
            options={'ordering': ['date_ordered']},
        ),
        migrations.RenameField(
            model_name='catalogproduct',
            old_name='accesories_cost',
            new_name='accessories_cost',
        ),
        migrations.RenameField(
            model_name='catalogproduct',
            old_name='accesories_margin',
            new_name='accessories_margin',
        ),
        migrations.RenameField(
            model_name='catalogproduct',
            old_name='percent_accesories_margin',
            new_name='percent_accessories_margin',
        ),
        migrations.AlterField(
            model_name='catalogaccessorydetail',
            name='catalog_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accessories_of_catalog_product', to='production.catalogproduct'),
        ),
        migrations.AlterField(
            model_name='catalogaccessorydetail',
            name='quantity',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='catalogaccessorydetail',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accessory_type_model', to='product.accessorytype'),
        ),
        migrations.AlterField(
            model_name='catalogelement',
            name='catalog_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='element_of_catalog_product', to='production.catalogproduct'),
        ),
        migrations.AlterField(
            model_name='catalogelement',
            name='element',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='element_type_model', to='product.element'),
        ),
        migrations.AlterField(
            model_name='catalogelement',
            name='quantity',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='catalogworktime',
            name='catalog_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='worktime_of_catalog_product', to='production.catalogproduct'),
        ),
        migrations.AlterField(
            model_name='catalogworktime',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=10, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='catalogworktime',
            name='duration',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='catalogworktime',
            name='worktime',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='worktime_type_model', to='product.worktimetype'),
        ),
        migrations.AlterField(
            model_name='orderproductionstage',
            name='production',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_stages', to='production.production'),
        ),
        migrations.AlterField(
            model_name='orderproductionstage',
            name='production_stage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_assignments', to='production.productionstage'),
        ),
        migrations.AlterField(
            model_name='production',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productions_customer', to='product.customer'),
        ),
        migrations.AlterField(
            model_name='production',
            name='object_id',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='production',
            name='production_stages',
            field=models.ManyToManyField(blank=True, related_name='production_stages', through='production.OrderProductionStage', to='production.productionstage'),
        ),
    ]
