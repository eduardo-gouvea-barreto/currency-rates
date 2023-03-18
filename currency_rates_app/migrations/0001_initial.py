# Generated by Django 4.1.7 on 2023-03-18 15:43

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currencies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('code', models.CharField(max_length=3, unique=True, validators=[django.core.validators.MinLengthValidator(3)])),
                ('symbol', models.CharField(max_length=3, unique=True)),
            ],
            options={
                'db_table': 'app_currencies',
            },
        ),
        migrations.CreateModel(
            name='RatesBaseDollar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('rate', models.DecimalField(decimal_places=4, max_digits=14)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='currency_rates_app.currencies')),
            ],
            options={
                'db_table': 'app_rates_base_dollar',
            },
        ),
    ]
