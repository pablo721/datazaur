from django.db import models


class CryptoPortfolio(models.Model):
    creator = models.ForeignKey('website.Account', related_name='users_portfolio', on_delete=models.CASCADE)
    name = models.CharField(max_length=32, default='Portfolio')
    currency = models.ForeignKey('data.Currency', on_delete=models.CASCADE, related_name='portfolio_currency',
                                 blank=True)
    coins = models.ManyToManyField('crypto.Cryptocurrency', related_name='portfolio_coins', blank=True,
                                   through='Amounts', through_fields=('portfolio', 'coin'))


class Amounts(models.Model):
    portfolio = models.ForeignKey('portfolio.CryptoPortfolio', on_delete=models.CASCADE, related_name='amounts_portfolio')
    coin = models.ForeignKey('crypto.Cryptocurrency', on_delete=models.CASCADE, related_name='amounts_coin')
    amount = models.FloatField(default=0)
    source = models.ForeignKey('crypto.CryptoExchange', blank=True, on_delete=models.CASCADE,
                               related_name='portfolio_source')
