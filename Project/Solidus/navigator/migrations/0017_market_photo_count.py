# Generated by Django 4.2.7 on 2023-11-26 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navigator', '0016_alter_category_id_alter_market_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='photo_count',
            field=models.DecimalField(decimal_places=0, max_digits=10, null=True),
        ),
    ]
