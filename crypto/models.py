from django.db import models
from config import constants


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
    countries = models.ManyToManyField('data.Country', related_name='exchange_countries', blank=True)
    currencies = models.ManyToManyField('data.Currency', related_name='exchange_currencies', blank=True)
    tickers = models.ManyToManyField('crypto.Cryptocurrency', related_name='exchange_tickers', blank=True)
    daily_vol = models.FloatField(null=True, blank=True)
    monthly_vol = models.FloatField(null=True, blank=True)


# portfolio attribute determines whether it is a watchlist (False) or portfolio (True)
# when portfolio=True, amounts of coins in portfolio can be set through PortfolioAmounts
class CryptoWatchlist(models.Model):
    creator = models.ForeignKey('website.Account', related_name='users_watchlists', on_delete=models.CASCADE)
    followers = models.ManyToManyField('website.Account', related_name='watchlist_followers', blank=True)
    name = models.CharField(max_length=32, default='Watchlist')
    currency = models.ForeignKey('data.Currency', on_delete=models.CASCADE, related_name='watchlist_currency',
                                 blank=True)
    coins = models.ManyToManyField('crypto.Cryptocurrency', related_name='watchlist_coins', blank=True,
                                   through='Amounts', through_fields=('watchlist', 'coin'))


class Amounts(models.Model):
    watchlist = models.ForeignKey('crypto.CryptoWatchlist', on_delete=models.CASCADE, related_name='amounts_watchlist')
    coin = models.ForeignKey('crypto.Cryptocurrency', on_delete=models.CASCADE, related_name='amounts_coin')
    amount = models.FloatField(default=0)
    source = models.ForeignKey('crypto.CryptoExchange', blank=True, on_delete=models.CASCADE,
                               related_name='watchlist_source')
