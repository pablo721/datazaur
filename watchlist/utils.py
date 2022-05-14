from .models import *



def generate_name(account):
	count = CryptoWatchlist.objects.filter(creator=account).count()
	return f'Watchlist {count + 1}'



	