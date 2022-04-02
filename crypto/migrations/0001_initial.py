# Generated by Django 4.0 on 2022-04-02 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Cryptocurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('symbol', models.CharField(max_length=32)),
                ('url', models.CharField(blank=True, max_length=256, null=True)),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
                ('hash_algorithm', models.CharField(blank=True, max_length=64, null=True)),
                ('proof_type', models.CharField(blank=True, max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CryptoExchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('grade', models.CharField(blank=True, choices=[(0, 'A'), (1, 'B'), (2, 'C'), (3, 'NA')], max_length=3, null=True)),
                ('url', models.CharField(blank=True, max_length=256, null=True)),
                ('daily_vol', models.FloatField(blank=True, null=True)),
                ('monthly_vol', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CryptoWatchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Watchlist', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='PrivateKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=256)),
                ('chain', models.CharField(max_length=64)),
                ('hash_algo', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='PublicKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=256)),
                ('chain', models.CharField(max_length=64)),
            ],
        ),
    ]
