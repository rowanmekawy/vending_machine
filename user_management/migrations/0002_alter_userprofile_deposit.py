# Generated by Django 4.1.7 on 2024-02-08 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='deposit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
