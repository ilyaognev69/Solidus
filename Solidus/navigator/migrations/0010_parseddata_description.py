# Generated by Django 3.0.14 on 2023-11-16 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navigator', '0009_parseddata_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='parseddata',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
