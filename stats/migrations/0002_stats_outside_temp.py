# Generated by Django 4.2 on 2023-04-28 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stats',
            name='outside_temp',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]
