# Generated by Django 2.2.7 on 2020-01-15 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment', '0003_overall_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='overall_rating',
            name='filename',
            field=models.CharField(max_length=100),
        ),
    ]
