# Generated by Django 4.0 on 2022-07-17 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('crypto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=64, unique=True)),
                ('value', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table', models.CharField(max_length=32)),
                ('timestamp', models.DateTimeField()),
                ('status', models.IntegerField()),
                ('message', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_code', models.CharField(default='USD', max_length=3)),
                ('signup_location', models.CharField(blank=True, max_length=64, null=True)),
                ('signup_ip', models.CharField(blank=True, max_length=45, null=True)),
                ('exchanges', models.ManyToManyField(blank=True, to='crypto.CryptoExchange')),
                ('friends', models.ManyToManyField(blank=True, to='website.Account')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_account', to='auth.user')),
            ],
        ),
    ]