# Generated by Django 4.0 on 2022-07-17 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('markets', '0001_initial'),
        ('watchlist', '0001_initial'),
        ('website', '0001_initial'),
        ('data', '0001_initial'),
        ('crypto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_watchlists', to='website.account'),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='tickers',
            field=models.ManyToManyField(blank=True, related_name='watchlist_coins', to='markets.Ticker'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='assets',
            field=models.ManyToManyField(blank=True, related_name='portfolio_assets', through='watchlist.Amounts', to='data.Asset'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='coins',
            field=models.ManyToManyField(blank=True, related_name='portfolio_coins', through='watchlist.Amounts', to='crypto.Cryptocurrency'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='commodities',
            field=models.ManyToManyField(blank=True, related_name='portfolio_commodities', through='watchlist.Amounts', to='data.Commodity'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_portfolio', to='website.account'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='currencies',
            field=models.ManyToManyField(blank=True, related_name='portfolio_assets', through='watchlist.Amounts', to='data.Currency'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='currency',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_currency', to='data.currency'),
        ),
        migrations.AddField(
            model_name='amounts',
            name='asset',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='amounts_asset', to='data.asset'),
        ),
        migrations.AddField(
            model_name='amounts',
            name='coin',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='amounts_coin', to='crypto.cryptocurrency'),
        ),
        migrations.AddField(
            model_name='amounts',
            name='commodity',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='amounts_commodity', to='data.commodity'),
        ),
        migrations.AddField(
            model_name='amounts',
            name='currency',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='amounts_currency', to='data.currency'),
        ),
        migrations.AddField(
            model_name='amounts',
            name='portfolio',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_crypto_amount', to='watchlist.portfolio'),
        ),
        migrations.AddField(
            model_name='amounts',
            name='source',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_source', to='crypto.cryptoexchange'),
        ),
    ]
