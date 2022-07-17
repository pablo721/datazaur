from django.db import models


class Watchlist(models.Model):
    creator = models.ForeignKey('website.Account', related_name='users_watchlists', on_delete=models.CASCADE)
    name = models.CharField(max_length=32, default='Watchlist')
    tickers = models.ManyToManyField('markets.Ticker', related_name='watchlist_coins', blank=True)



class Portfolio(models.Model):
    creator = models.ForeignKey('website.Account', related_name='users_portfolio', on_delete=models.CASCADE)
    creation_date = models.DateTimeField()
    name = models.CharField(max_length=32, default='Portfolio')
    currency = models.ForeignKey('data.Currency', on_delete=models.CASCADE, related_name='portfolio_currency',
                                 blank=True)
    assets = models.ManyToManyField('data.Asset', related_name='portfolio_assets', blank=True,
                                   through='Amounts', through_fields=('portfolio', 'asset', 'amount', 'asset_class', 'source'))
    coins = models.ManyToManyField('crypto.Cryptocurrency', related_name='portfolio_coins', blank=True,
                                   through='Amounts', through_fields=('portfolio', 'coin', 'amount', 'asset_class', 'source'))
    currencies = models.ManyToManyField('data.Currency', related_name='portfolio_assets', blank=True,
                                   through='Amounts', through_fields=('portfolio', 'currency', 'amount', 'asset_class', 'source'))
    commodities = models.ManyToManyField('data.Commodity', related_name='portfolio_commodities', blank=True,
                                   through='Amounts', through_fields=('portfolio', 'commodity', 'amount', 'asset_class', 'source'))



class Amounts(models.Model):
    portfolio = models.OneToOneField('watchlist.Portfolio', on_delete=models.CASCADE, related_name='portfolio_crypto_amount')
    asset = models.ForeignKey('data.Asset', related_name='amounts_asset', blank=True, on_delete=models.CASCADE)
    coin = models.ForeignKey('crypto.Cryptocurrency', related_name='amounts_coin', blank=True, on_delete=models.CASCADE)
    currency = models.ForeignKey('data.Currency', related_name='amounts_currency', blank=True, on_delete=models.CASCADE)
    commodity = models.ForeignKey('data.Commodity', related_name='amounts_commodity', blank=True, on_delete=models.CASCADE)
    asset_class = models.CharField(max_length=32)
    amount = models.FloatField(default=0)
    source = models.ForeignKey('crypto.CryptoExchange', blank=True, on_delete=models.CASCADE,
                               related_name='portfolio_source')

