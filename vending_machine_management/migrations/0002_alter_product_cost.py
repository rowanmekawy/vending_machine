# Generated by Django 4.2.10 on 2024-02-09 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vending_machine_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]