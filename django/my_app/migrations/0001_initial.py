# Generated by Django 5.0.4 on 2024-04-24 21:25

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={
                'verbose_name': 'Kategoriyalar',
                'verbose_name_plural': 'Kategoriya',
            },
        ),
        migrations.CreateModel(
            name='CategoryRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(blank=True, max_length=25, null=True)),
                ('car_count', models.IntegerField(default=0)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_app.category')),
            ],
            options={
                'verbose_name': 'Regionlar',
                'verbose_name_plural': 'Region',
            },
        ),
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parking_count', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('is_active', models.BooleanField(default=False)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_app.category')),
            ],
            options={
                'verbose_name': 'Parking',
                'verbose_name_plural': 'Parking',
            },
        ),
        migrations.CreateModel(
            name='Auto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_name', models.CharField(blank=True, max_length=25, null=True)),
                ('car_id', models.CharField(blank=True, max_length=25, null=True)),
                ('car_qr', models.ImageField(blank=True, null=True, upload_to='qr/')),
                ('is_active', models.BooleanField()),
                ('lat', models.FloatField(blank=True, null=True)),
                ('long', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_app.categoryregion')),
                ('parking_number', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='autos', to='my_app.parking')),
            ],
            options={
                'verbose_name': 'Car',
                'verbose_name_plural': 'Cars',
            },
        ),
    ]