# Generated by Django 5.0.4 on 2024-04-21 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worktimetype',
            name='workers',
        ),
        migrations.AddField(
            model_name='worktime',
            name='workers',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]