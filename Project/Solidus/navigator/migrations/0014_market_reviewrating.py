# Generated by Django 3.0.14 on 2023-11-23 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navigator', '0013_market'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='reviewRating',
            field=models.DecimalField(decimal_places=1, max_digits=10, null=True),
        ),
    ]
