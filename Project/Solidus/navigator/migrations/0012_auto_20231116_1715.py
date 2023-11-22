# Generated by Django 3.0.14 on 2023-11-16 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navigator', '0011_parseddata_website'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('slug', models.SlugField(max_length=200, null=True)),
                ('picture_url', models.URLField(null=True)),
                ('url', models.URLField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('website', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='ParsedData',
        ),
    ]
