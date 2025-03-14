# Generated by Django 5.0 on 2024-10-16 17:33

import django.db.models.deletion
import product.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_newproject_worktime_cost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=60, null=True)),
                ('phone_number', models.IntegerField()),
                ('street', models.CharField(max_length=100, null=True)),
                ('code', models.CharField(max_length=15, null=True)),
                ('city', models.CharField(max_length=40, null=True)),
                ('email', models.EmailField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('document', models.ImageField(upload_to=product.models.documents_user_directory_path)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.FileField(upload_to=product.models.documents_user_directory_path)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='newproject',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.customer'),
        ),
        migrations.AddField(
            model_name='newproject',
            name='document',
            field=models.ManyToManyField(blank=True, null=True, to='product.document'),
        ),
        migrations.AddField(
            model_name='newproject',
            name='image',
            field=models.ManyToManyField(blank=True, null=True, to='product.image'),
        ),
    ]
