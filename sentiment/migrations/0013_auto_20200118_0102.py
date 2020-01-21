# Generated by Django 2.2.7 on 2020-01-17 19:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sentiment', '0012_auto_20200117_1834'),
    ]

    operations = [
        migrations.CreateModel(
            name='overall_rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=100)),
                ('process_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('rating', models.FloatField(default=0.0)),
                ('positive', models.FloatField()),
                ('negative', models.FloatField()),
                ('neutral', models.FloatField()),
                ('rat', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='overall_rating1',
        ),
    ]