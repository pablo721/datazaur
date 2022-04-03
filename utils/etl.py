import pandas as pd
from crypto.models import *
from markets.models import *
from news.models import *
from data.models import *


def watchlist_prices(watchlist, quote):
	result = pd.DataFrame(index=[], data={'name': [], 'amount': [], 'bid': [], 'ask': [], 'daily_delta': [],
													  'daily_vol': [], 'daily_low': [], 'daily_high': []})
	n = 0
	for coin in watchlist.coins.all():
		if Ticker.objects.filter(base=coin.symbol).filter(quote=quote).exists():
			n += 1
			result.loc[coin.symbol] = Ticker.objects.get(base=coin.symbol, quote=quote).__dict__
			if Amounts.objects.filter(watchlist=watchlist).filter(coin=coin).exists():
				result.loc[coin.symbol, 'amount'] = Amounts.objects.get(watchlist=watchlist, coin=coin).amount
			print(result.loc[coin.symbol])
	print(f'Found {n} out of {watchlist.coins.all().count()} prices.')
	return result


