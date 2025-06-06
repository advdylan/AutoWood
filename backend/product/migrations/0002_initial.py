# Generated by Django 5.0 on 2025-05-10 20:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('production', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newproject',
            name='production_stages',
            field=models.ManyToManyField(blank=True, to='production.productionstage'),
        ),
        migrations.AddField(
            model_name='image',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.newproject'),
        ),
        migrations.AddField(
            model_name='document',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='product.newproject'),
        ),
        migrations.AddField(
            model_name='accessorydetail',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_accesories', to='product.newproject'),
        ),
        migrations.AddField(
            model_name='newprojectelement',
            name='element',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.element'),
        ),
        migrations.AddField(
            model_name='newprojectelement',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_elements', to='product.newproject'),
        ),
        migrations.AddField(
            model_name='newproject',
            name='new_elements',
            field=models.ManyToManyField(blank=True, through='product.NewProjectElement', to='product.element'),
        ),
        migrations.AddField(
            model_name='newproject',
            name='paints',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.paints'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category'),
        ),
        migrations.AddField(
            model_name='product',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.collection'),
        ),
        migrations.AddField(
            model_name='product',
            name='elements',
            field=models.ManyToManyField(to='product.element'),
        ),
        migrations.AddField(
            model_name='product',
            name='paints',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.paints'),
        ),
        migrations.AddField(
            model_name='balance',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
        migrations.AddField(
            model_name='projectworktime',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_worktime', to='product.newproject'),
        ),
        migrations.AddField(
            model_name='newproject',
            name='wood',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.wood'),
        ),
        migrations.AddField(
            model_name='element',
            name='wood_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.wood'),
        ),
        migrations.AddField(
            model_name='projectworktime',
            name='worktime',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.worktimetype'),
        ),
        migrations.AddField(
            model_name='newproject',
            name='worktimes',
            field=models.ManyToManyField(blank=True, through='product.ProjectWorktime', to='product.worktimetype'),
        ),
    ]
