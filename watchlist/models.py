from django.db import models




class CryptoWatchlist(models.Model):
    creator = models.ForeignKey('website.Account', related_name='users_watchlists', on_delete=models.CASCADE)
    followers = models.ManyToManyField('website.Account', related_name='watchlist_followers', blank=True)
    name = models.CharField(max_length=32, default='Watchlist')
    currency = models.ForeignKey('data.Currency', on_delete=models.CASCADE, related_name='watchlist_currency',
                                 blank=True)
    coins = models.ManyToManyField('crypto.Cryptocurrency', related_name='watchlist_coins', blank=True,
                                   through='Amounts', through_fields=('watchlist', 'coin'))