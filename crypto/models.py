from django.db import models
from data import constants



class PrivateKey(models.Model):
    key = models.CharField(max_length=256)
    chain = models.CharField(max_length=64)
    hash_algo = models.CharField(max_length=64)
    user = models.ForeignKey('website.Account', related_name='users_privkey', on_delete=models.CASCADE)
    pub_key = models.OneToOneField('crypto.PublicKey', related_name='pub_privkey', on_delete=models.CASCADE)


class PublicKey(models.Model):
    key = models.CharField(max_length=256)
    chain = models.CharField(max_length=64)
    user = models.ForeignKey('website.Account', related_name='users_pubkey', on_delete=models.CASCADE)



class Cryptocurrency(models.Model):
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=32)
    url = models.CharField(max_length=256, null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    hash_algorithm = models.CharField(max_length=64, null=True, blank=True)
    proof_type = models.CharField(max_length=32, null=True, blank=True)


# crypto/crypto ticker e.g. ETH/BTC
class CryptoTicker(models.Model):
    base = models.CharField(max_length=16)
    quote = models.CharField(max_length=16)
    bid = models.FloatField(blank=True, null=True)
    ask = models.FloatField(blank=True, null=True)
    daily_delta = models.FloatField(blank=True, null=True)
    daily_vol = models.FloatField(blank=True, null=True)
    daily_low = models.FloatField(blank=True, null=True)
    daily_high = models.FloatField(blank=True, null=True)



# crypto/fiat ticker e.q. ETH/USD
class CryptoFiatTicker(models.Model):
    base = models.CharField(max_length=16)
    quote = models.CharField(max_length=3)
    bid = models.FloatField(blank=True, null=True)
    ask = models.FloatField(blank=True, null=True)
    daily_delta = models.FloatField(blank=True, null=True)
    daily_vol = models.FloatField(blank=True, null=True)
    daily_low = models.FloatField(blank=True, null=True)
    daily_high = models.FloatField(blank=True, null=True)


# class NFT(models.Model):
#     name = models.CharField(max_length=64, blank=False, null=False)
#     symbol = models.CharField(max_length=32)
#     floor_price = models.FloatField()
#     quote_curr = models.CharField(max_length=16)
#     collection = models.ForeignKey('crypto.NFTCollection', on_delete=models.CASCADE)
#
#
# class NFTCollection(models.Model):
#     name = models.CharField(max_length=128)
#     symbol = models.CharField(max_length=32)


class CryptoExchange(models.Model):
    name = models.CharField(max_length=128)
    grade = models.CharField(choices=enumerate(constants.CRYPTO_EXCHANGE_GRADES), max_length=3, null=True, blank=True)
    url = models.CharField(max_length=256, null=True, blank=True)
    countries = models.ManyToManyField('economics.Country', related_name='exchange_countries', blank=True)
    currencies = models.ManyToManyField('markets.Currency', related_name='exchange_currencies', blank=True)
    tickers = models.ManyToManyField('crypto.Cryptocurrency', related_name='exchange_tickers', blank=True)
    daily_vol = models.FloatField(null=True, blank=True)
    monthly_vol = models.FloatField(null=True, blank=True)


# portfolio attribute determines whether it is a watchlist (False) or portfolio (True)
# when portfolio=True, amounts of coins in portfolio can be set through PortfolioAmounts
class CryptoWatchlist(models.Model):
    creator = models.ForeignKey('website.Account', related_name='users_watchlists', on_delete=models.CASCADE)
    followers = models.ManyToManyField('website.Account', related_name='watchlist_followers', blank=True)
    name = models.CharField(max_length=32, default='Watchlist')
    currency = models.ForeignKey('markets.Currency', on_delete=models.CASCADE, related_name='watchlist_currency',
                                 blank=True)
    coins = models.ManyToManyField('crypto.Cryptocurrency', related_name='watchlist_coins', blank=True,
                                   through='PortfolioAmounts', through_fields=('watchlist', 'coin'))


class PortfolioAmounts(models.Model):
    watchlist = models.ForeignKey('crypto.CryptoWatchlist', on_delete=models.CASCADE, related_name='portfolioamounts_watchlist')
    coin = models.ForeignKey('crypto.Cryptocurrency', on_delete=models.CASCADE, related_name='portfolioamounts_coin')
    amount = models.FloatField(default=0)
    source = models.ForeignKey('crypto.CryptoExchange', blank=True, on_delete=models.CASCADE,
                               related_name='watchlist_source')
